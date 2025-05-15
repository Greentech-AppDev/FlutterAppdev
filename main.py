from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class SensorData(BaseModel):
    temperature: float
    humidity: float

# Store the latest sensor data in a list (simple in-memory storage)
data_history: List[SensorData] = []
MAX_HISTORY = 10

@app.post("/temperature")
def receive_data(data: SensorData):
    global data_history
    # Append new data to the history
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
    # Return the entire history
    return [{"temperature": data.temperature, "humidity": data.humidity} for data in data_history]
