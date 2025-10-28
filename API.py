import zoneinfo
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from mlp import MLP
import numpy as np

app = FastAPI()

# load the pre-trained model
MLP_e5 = MLP(n_features=8, output_size=1, n_hidden=2, hidden_size=16)
MLP_e5.load_weights("best_model_weights_e5.npz")
MLP_e10 = MLP(n_features=8, output_size=1, n_hidden=2, hidden_size=16)
MLP_e10.load_weights("best_model_weights_e10.npz")
MLP_diesel = MLP(n_features=8, output_size=1, n_hidden=2, hidden_size=16)
MLP_diesel.load_weights("best_model_weights_diesel.npz")
MODELS = {"e5": MLP_e5, "e10": MLP_e10, "diesel": MLP_diesel}

# load geo scaling for geo features
_coords_df = pd.read_csv(
    "training_data/station_uuid_to_coordinates.csv",
    usecols=["uuid", "latitude", "longitude"],
    dtype={"uuid": "string", "latitude": np.float32, "longitude": np.float32},
)
COORD_MAP = dict(
    zip(_coords_df["uuid"], zip(_coords_df["latitude"], _coords_df["longitude"]))
)

# load geo scaler
_geo = np.load("geo_scaler.npz", allow_pickle=True)
LAT_MEAN, LAT_STD = float(_geo["lat_mean"]), max(float(_geo["lat_std"]), 1e-8)
LON_MEAN, LON_STD = float(_geo["lon_mean"]), max(float(_geo["lon_std"]), 1e-8)


# allowed origins for CORS
origins = ["http://localhost:8081", "http://127.0.0.1:8081", "http://192.168.0.10:8081"]

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


# request for fuel price prediction
@app.get("/predict")
def predict(fuel_station: str, fuel_type: str, time_frame: str):
    # choose model
    key = fuel_type.strip().lower()
    model = MODELS.get(key)
    if model is None:
        raise HTTPException(status_code=400, detail=f"Unknown fuel type: {fuel_type}")

    # Collect the predictions over the timeframe
    price_predictions = []

    # geo features

    return {
        "fuel_station": fuel_station,
        "fuel_type": fuel_type,
        "time_frame": time_frame,
    }
