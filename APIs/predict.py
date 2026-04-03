from datetime import date
import os
import zoneinfo
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import requests
from APIs.tk_client import get_info_from_station
from model.mlp import MLP
import numpy as np
import dotenv

dotenv.load_dotenv()  # load environment variables from .env file

app = FastAPI()

tk_api_key = os.getenv("api_key")

# allowed origins for CORS
origins = ["http://localhost:8081", "http://localhost:8082", "http://127.0.0.1:8081", "http://192.168.0.10:8081", "http://192.168.178.64:8081"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/stations/{city}")
def get_info(city: str):
    print(f"API called for city: {city}")
    return get_info_from_station(city)

# request for fuel price prediction
# @app.get("/predict")
# def predict(fuel_type: str, station_uuid: str):
    