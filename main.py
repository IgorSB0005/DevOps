from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import os

app = FastAPI()

DB_PATH = "/app/data/database.db"

class Car(BaseModel):
    brand: str
    model: str

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS cars (id INTEGER PRIMARY KEY AUTOINCREMENT, brand TEXT, model TEXT)')
    conn.commit()
    conn.close()

init_db()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/status")
def get_status():
    return {"status": "ok", "version": "1.0.0"}

@app.get("/cars")
def get_cars():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT brand, model FROM cars')
    cars = [{"brand": row[0], "model": row[1]} for row in cursor.fetchall()]
    conn.close()
    return {"cars": cars}

@app.post("/cars")
def add_car(car: Car):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO cars (brand, model) VALUES (?, ?)', (car.brand, car.model))
    conn.commit()
    conn.close()
    return {"message": "Car added successfully!"}