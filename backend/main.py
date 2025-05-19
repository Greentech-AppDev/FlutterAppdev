from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from routes import auth
from auth import (
    create_access_token, get_password_hash, verify_password, get_current_user,
    router as auth_router, SECRET_KEY, ALGORITHM
)
from models import UserIn, UserOut, Token, User            # ⬅️ removed Temperature
from database import get_db                                # ⬅️ removed SessionLocal

app = FastAPI()

# ── CORS ──────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── OAuth2 / auth routes ─────────────────────────────────────────────
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app.include_router(auth_router)

# ── In‑memory sensor storage ──────────────────────────────────────────
class SensorData(BaseModel):
    temperature: float          # water temp from ESP32
    humidity: float             # air temp from ESP32
    ts: Optional[str] = None

data_history: List[SensorData] = []
MAX_HISTORY = 10

# ── ESP32 POSTs readings here ────────────────────────────────────────
@app.post("/temperature")
def receive_data(data: SensorData, user: str = Depends(get_current_user)):
    data.ts = datetime.utcnow().isoformat()
    data_history.append(data)
    if len(data_history) > MAX_HISTORY:
        data_history.pop(0)
    print(f"Received temperature={data.temperature}, humidity={data.humidity}")
    return {"message": "Data received successfully"}

# ── Flutter dashboard polls this every 3 s ───────────────────────────
@app.get("/temperature/latest")
def latest_temperature(user: str = Depends(get_current_user)):
    if not data_history:
        raise HTTPException(status_code=404, detail="No readings yet")
    row = data_history[-1]
    return {
        "water_temperature": row.temperature,
        "air_temperature":  row.humidity,
        "ts":               row.ts,
    }

# (Optional) full history
@app.get("/temperature/history")
def get_data_history(user: str = Depends(get_current_user)):
    if not data_history:
        raise HTTPException(status_code=404, detail="No readings yet")
    return data_history

# ── User registration / login (unchanged) ────────────────────────────
@app.post("/register", response_model=Token)
def register(user: UserIn, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = get_password_hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"access_token": create_access_token(data={"sub": str(new_user.id)}),
            "token_type": "bearer"}

@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": create_access_token(data={"sub": str(user.id)}),
            "token_type": "bearer"}

# ── Misc routes ──────────────────────────────────────────────────────
@app.get("/protected")
def read_protected(token: str = Depends(oauth2_scheme)):
    return {"message": "Protected route access granted!"}

@app.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=400, detail="Invalid token")

        user = db.query(User).filter(User.id == int(user_id)).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.is_verified = True
        db.commit()
        return {"message": "Email successfully verified"}
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")
