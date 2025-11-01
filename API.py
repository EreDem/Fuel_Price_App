from datetime import date
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
    "station_uuid_to_coordinates.csv",
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
def predict(fuel_type: str, station_uuid: str):
    # choose model
    key = fuel_type.strip().lower()
    model = MODELS.get(key)
    if model is None:
        raise HTTPException(status_code=400, detail=f"Unknown fuel type: {fuel_type}")

    # geo features
    station_lat, station_lon = COORD_MAP.get(station_uuid, (LAT_MEAN, LON_MEAN))

    # normalize geo features
    norm_lat = (station_lat - LAT_MEAN) / LAT_STD
    norm_lon = (station_lon - LON_MEAN) / LON_STD

    # start time
    start_time = pd.Timestamp.now(tz=zoneinfo.ZoneInfo("Europe/Berlin"))

    time_to_price = []

    for t in range(144):  # next 72 hours in 30-min intervals
        # build time features
        current_time = start_time + pd.Timedelta(minutes=30 * t)

        # Hour + Minute as decimal hour (e.g., 13.5 for 13:30)
        hour = current_time.hour + current_time.minute / 60.0

        # Weekday (0 = Monday, 6 = Sunday)
        weekday = current_time.weekday()

        # Day of year (1–365/366)
        day_of_year = current_time.dayofyear

        # cyclic features
        hour_sin = np.sin(2 * np.pi * hour / 24)
        hour_cos = np.cos(2 * np.pi * hour / 24)
        weekday_sin = np.sin(2 * np.pi * weekday / 7)
        weekday_cos = np.cos(2 * np.pi * weekday / 7)
        day_of_year_sin = np.sin(2 * np.pi * day_of_year / 365)
        day_of_year_cos = np.cos(2 * np.pi * day_of_year / 365)

        # assemble feature vector
        X_input = np.array(
            [
                hour_sin,
                hour_cos,
                weekday_sin,
                weekday_cos,
                day_of_year_sin,
                day_of_year_cos,
                norm_lat,
                norm_lon,
            ],
            dtype=np.float32,
        ).reshape(1, -1)

        # predict price
        price_pred = model.feed_forward(X_input)
        price = float(price_pred)

        decimal_time = (hour) % 24  # 0..24, bei 25 -> 1 usw.

        time_to_price.append(
            {
                "time": round(decimal_time, 3),
                "price": price,
            }
        )

    return {
        "predictions": time_to_price
    }
