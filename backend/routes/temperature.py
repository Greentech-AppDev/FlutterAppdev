from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import Reading, User              # adjust if your models import path differs
from database import get_db                  # already present in backend/
from auth import auth                        # your existing auth dependency

router = APIRouter(prefix="/temperature", tags=["temperature"])

@router.get("/latest")
def latest_temperature(db: Session = Depends(get_db),
                       current_user: User = Depends(auth)):
    """
    Return the most recent Reading row.
    """
    row = db.query(Reading).order_by(Reading.id.desc()).first()
    if row is None:
        return {"detail": "No readings yet"}
    return {
        "water_temperature": row.water_temp,
        "air_temperature":  row.air_temp,
        "ts":               row.created_at.isoformat()
    }
