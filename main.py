from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from routes import auth
from auth import create_access_token, get_password_hash, verify_password, get_current_user
from models import UserIn, UserOut, Token
from auth import verify_password
from models import User
from sqlalchemy.orm import Session
from database import get_db

app = FastAPI()



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(auth.router)


class SensorData(BaseModel):
    temperature: float
    humidity: float
    timestamp: Optional[str] = None

# Store the latest sensor data in a list (simple in-memory storage)
data_history: List[SensorData] = []
MAX_HISTORY = 10

@app.post("/temperature")
def receive_data(data: SensorData, user: str = Depends(get_current_user)):
    global data_history
    # Append new data to the history
    data.timestamp = datetime.utcnow().isoformat()
    data_history.append(data)
    # Keep only the last MAX_HISTORY entries
    if len(data_history) > MAX_HISTORY:
        data_history.pop(0)
    print(f"Received temperature: {data.temperature}, humidity: {data.humidity}")
    return {"message": "Data received successfully"}

@app.get("/temperature")
def get_latest_data():
    if not data_history:
        return {"message": "No data received yet"}
    # Return the latest data point
    latest_data = data_history[-1]
    return {"temperature": latest_data.temperature, "humidity": latest_data.humidity}

@app.get("/history")
def get_data_history():
    if not data_history:
        return {"message": "No data received yet"}
    return data_history  # Returns list of SensorData with temp, humidity, timestamp


@app.post("/register", response_model=UserOut)
def register(user: UserIn, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = get_password_hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"email": new_user.email}

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
