from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from routes import auth
from auth import create_access_token, get_password_hash, verify_password, get_current_user
from models import UserIn, UserOut, Token
from models import User
from sqlalchemy.orm import Session
from database import get_db
from jose import JWTError, jwt
from auth import SECRET_KEY, ALGORITHM

app = FastAPI()

router = APIRouter()
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
    data.timestamp = datetime.utcnow().isoformat()
    data_history.append(data)
    if len(data_history) > MAX_HISTORY:
        data_history.pop(0)
    print(f"Received temperature: {data.temperature}, humidity: {data.humidity}")
    return {"message": "Data received successfully"}

@app.get("/temperature")
def get_latest_data():
    if not data_history:
        return {"message": "No data received yet"}
    latest_data = data_history[-1]
    return {"temperature": latest_data.temperature, "humidity": latest_data.humidity}

@app.get("/history")
def get_data_history():
    if not data_history:
        return {"message": "No data received yet"}
    return data_history

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

    # ✅ Allow unverified users to get a token only to verify their email
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/protected")
def read_protected(token: str = Depends(oauth2_scheme)):
    return {"message": "Protected route access granted!"}

# ✅ New route for email verification
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
