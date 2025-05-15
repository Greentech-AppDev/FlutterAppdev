from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class SensorData(BaseModel):
    temperature: float
    humidity: float

# Store the latest sensor data globally (simple in-memory storage)
latest_data: Optional[SensorData] = None

@app.post("/temperature")
def receive_data(data: SensorData):
    global latest_data
    latest_data = data
    print(f"Received temperature: {data.temperature}, humidity: {data.humidity}")
    return {"message": "Data received successfully"}

@app.get("/temperature")
def get_latest_data():
    if latest_data is None:
        return {"message": "No data received yet"}
    return {"temperature": latest_data.temperature, "humidity": latest_data.humidity}

