from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3 as sql

app = FastAPI()

db = sql.connect('hackathon.db')

class User(BaseModel):
    name: str
    email: str
    id: str

class Measurement(BaseModel):
    user_id: str
    temperature: float
    heartrate: float
    respiratory_frequency: float
    movement: float
    snores: float

@app.get("/get_users")
async def get_users():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return [{"id": user[0], "name": user[1], "email": user[2]} for user in users]

@app.post("/register_user")
async def register(user: User):
    cursor = db.cursor()
    cursor.execute("Insert into users (id, name, email) values (?, ?, ?)", (user.id, user.name, user.email))
    db.commit()
    return {"message": "Registration successful"}


@app.post("/register_measurement")
async def register_measurement(measurement: Measurement):
    cursor = db.cursor()
    cursor.execute(""" Insert into measurements (user_id, temperature, heartrate, respiratory_frequency, movement, snores) values (?,?,?,?,?,?) """,
                   (measurement.user_id,
                    measurement.temperature,
                    measurement.heartrate,
                    measurement.respiratory_frequency,
                    measurement.movement,
                    measurement.snores))
    db.commit()
    return {"message": "success"}

@app.get("/get_measurements/{user_id}")
async def get_measurements(user_id: str):
    cursor = db.cursor()
    # we get our fields 
    cursor.execute("SELECT * FROM measurements WHERE user_id = ?", (user_id,))
    measurements = cursor.fetchall()
    return [{"timestamp": measurement[0], "temperature": measurement[1], "heartrate": measurement[2], "respiratory_frequency": measurement[3], "movement": measurement[4], "snores": measurement[5]} for measurement in measurements]


@app.get("/get_average/{user_id}/{start_time}/{end_time}")
async def get_average_time_frame(user_id: str, start_time: str, end_time: str):
    cursor = db.cursor()
    cursor.execute("""SELECT 
        AVG(temperature) as temperature,
        AVG(heartrate) as heartrate,
        AVG(respiratory_frequency) as respiratory_frequency,
        AVG(snores) as snores 
        FROM measurements WHERE user_id = ? AND timestamp BETWEEN ? AND ?""", (user_id, start_time, end_time))
    average = cursor.fetchone()

    if average == None:
        return {"error": "No measurements found within this time frame"}

    return {
        "temperature": average[0],
        "heartrate": average[1],
        "respiratory_frequency": average[2],
        "snores": average[3] 
    }
