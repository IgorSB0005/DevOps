from fastapi import FastAPI
from pydantic import BaseModel
import redis
import os
import json

app = FastAPI()

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
cache = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

class Car(BaseModel):
    brand: str
    model: str

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/status")
def get_status():
    return {"status": "ok", "version": "1.0.0"}

@app.get("/cars")
def get_cars():
    cars = cache.lrange("cars_list", 0, -1)
    return {"cars": [json.loads(car) for car in cars]}

@app.post("/cars")
def add_car(car: Car):
    cache.rpush("cars_list", json.dumps(car.dict()))
    return {"message": "Car added to Redis!"}

@app.get("/new")
def get_cars():
    return {"status": "GOOD TEST"}