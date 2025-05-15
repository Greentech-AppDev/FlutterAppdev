from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import datetime

app = FastAPI()

class TemperatureData(BaseModel):
    temperature: float
    timestamp: datetime.datetime

db: List[TemperatureData] = []

@app.post("/temperature")
def post_temperature(data: TemperatureData):
    db.append(data)
    return {"message": "Data received"}

@app.get("/temperature")
def get_temperature():
    return db
 
