from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas, auth, email_utils
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=schemas.UserOut)
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_password)

    # Generate persistent token and store
    access_token = auth.create_access_token(data={"sub": new_user.email})
    new_user.token = access_token

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Optionally send email verification
    # await email_utils.send_verification_email(new_user.email, access_token)

    return new_user

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not user.is_verified:
        raise HTTPException(status_code=400, detail="Email not verified")

    access_token = auth.create_access_token(data={"sub": user.email})
    user.token = access_token  # Store new token
    db.commit()

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/esp-token")
def get_token_for_esp(user: str = Query(...), db: Session = Depends(get_db)):
    user_obj = db.query(models.User).filter(models.User.email == user).first()
    if not user_obj or not user_obj.token:
        raise HTTPException(status_code=404, detail="Token not found")
    return {"access_token": user_obj.token}

@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    # decode token to get email, validate, update user.is_verified = True
    pass
