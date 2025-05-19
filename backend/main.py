from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from jose import JWTError, jwt
from sqlalchemy.orm import Session

# ─── local imports ────────────────────────────────────────────────────────────
from routes import auth                                # existing auth router
from auth import (
    create_access_token,
    get_password_hash,
    verify_password,
    get_current_user,
    router as auth_router,
    SECRET_KEY,
    ALGORITHM,
)
from models import UserIn, UserOut, Token, User
from database import get_db

# ─── app setup ────────────────────────────────────────────────────────────────
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# register the existing auth routes
app.include_router(auth_router)

# ─── in‑memory sensor storage (keeps last 10) ────────────────────────────────
class SensorData(BaseModel):
    water_temperature: float  # ESP32 sends "temperature" → water temp
    air_temperature:  float   # ESP32 sends "humidity"    → air temp
    ts: Optional[str] = None  # ISO timestamp

data_history: List[SensorData] = []
MAX_HISTORY = 10

# ─── endpoints used by ESP32 ─────────────────────────────────────────────────
@app.post("/temperature")
def receive_data(data: SensorData, user: str = Depends(get_current_user)):
    """
    ESP32 POSTs JSON: {"water_temperature":22.3,"air_temperature":26.0}
    """
    data.ts = datetime.utcnow().isoformat()
    data_history.append(data)
    if len(data_history) > MAX_HISTORY:
        data_history.pop(0)
    print(
        f"Received water_temp={data.water_temperature}, "
        f"air_temp={data.air_temperature}"
    )
    return {"message": "Data received successfully"}

# ─── latest reading for Flutter dashboard ────────────────────────────────────
@app.get("/temperature/latest")
def latest_temperature(user: str = Depends(get_current_user)):
    """
    Return the most recent sensor reading (water & air temperature).
    """
    if not data_history:
        return {"detail": "No readings yet"}
    row = data_history[-1]
    return {
        "water_temperature": row.water_temperature,
        "air_temperature":  row.air_temperature,
        "ts":               row.ts,
    }

# ─── optional helpers ────────────────────────────────────────────────────────
@app.get("/temperature/history")
def get_data_history(user: str = Depends(get_current_user)):
    """
    Return up to the last 10 readings.
    """
    if not data_history:
        return {"detail": "No readings yet"}
    return data_history

# ─── auth, register, token, verify routes (unchanged) ───────────────────────
@app.post("/register", response_model=Token)
def register(user: UserIn, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = get_password_hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token(data={"sub": str(new_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


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
