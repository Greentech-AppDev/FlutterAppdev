from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import datetime

app = FastAPI()

class SensorData(BaseModel):
    temperature: float
    humidity: float

@app.post("/temperature")
def receive_data(data: SensorData):
    print(f"Received temperature: {data.temperature}, humidity: {data.humidity}")
    return {"message": "Data received successfully"}
