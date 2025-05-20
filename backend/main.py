from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from routes import auth
from auth import get_current_user, router as auth_router, SECRET_KEY, ALGORITHM
from models import User, Token
from database import get_db

app = FastAPI()

# ── CORS ─────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 👈 Change to specific frontend domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Auth ─────────────────────────────────────────────────────
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app.include_router(auth_router)

# ── Sensor Model ─────────────────────────────────────────────
class SensorData(BaseModel):
    temperature: float
    humidity: float
    ts: Optional[str] = None

data_history: List[SensorData] = []
MAX_HISTORY = 10

@app.post("/temperature")
def receive_data(data: SensorData, user: str = Depends(get_current_user)):
    data.ts = datetime.utcnow().isoformat()
    data_history.append(data)
    if len(data_history) > MAX_HISTORY:
        data_history.pop(0)
    print(f"Received temperature={data.temperature}, humidity={data.humidity}")
    return {"message": "Data received successfully"}

@app.get("/temperature/latest")
def latest_temperature(user: str = Depends(get_current_user)):
    if not data_history:
        raise HTTPException(status_code=404, detail="No readings yet")
    row = data_history[-1]
    return {
        "water_temperature": row.temperature,
        "air_temperature": row.humidity,
        "ts": row.ts,
    }

@app.get("/temperature/history")
def get_data_history(user: str = Depends(get_current_user)):
    if not data_history:
        raise HTTPException(status_code=404, detail="No readings yet")
    return data_history

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
        raise HTTPException(status_code=400, detail="Invalid token"})
