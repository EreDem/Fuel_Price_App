import numpy as np
from mlp import MLP
from mlp import Trainer
import pandas as pd


# normalize coordinate features and save scaler parameters
coords = pd.read_csv(
    "training_data/station_uuid_to_coordinates.csv", usecols=["latitude", "longitude"]
)
lat_mean, lat_std = coords["latitude"].mean(), coords["latitude"].std()
lon_mean, lon_std = coords["longitude"].mean(), coords["longitude"].std()

np.savez(
    "geo_scaler.npz",
    lat_mean=lat_mean,
    lat_std=lat_std,
    lon_mean=lon_mean,
    lon_std=lon_std,
)


# get data chunk and preprocess
def get_data_chunk(year: str, month: str, day: str):
    # load data from file
    file_path = f"training_data/{year}/{month}/{year}-{month}-{day}-prices.csv"

    #### create features and labels

    ## date features
    # get first col (date col) of csv
    date = pd.read_csv(file_path, usecols=["date"], parse_dates=[0])

    # time is given with time zone, which we do not need
    date["date"] = pd.to_datetime(date["date"], errors="coerce")
    date["date"] = date["date"].dt.tz_localize(None)

    # n_before = len(date)
    # date.dropna(subset=["date"], inplace=True)
    # if len(date) < n_before:
    #     print(f"⚠️ {n_before - len(date)} ungültige Datumswerte entfernt")
    # if len(date) == 0:
    #     print(f"⚠️ Keine gültigen Daten am, wird übersprungen.")
    #     return None, None, None, None, None, None

    ### extract time components
    # Hour + Minute as decimal hour (e.g., 13.5 for 13:30)
    hour = date["date"].dt.hour + date["date"].dt.minute / 60.0

    # Weekday (0 = Monday, 6 = Sunday)
    weekday = date["date"].dt.weekday

    # Day of year (1–365/366)
    day_of_year = date["date"].dt.dayofyear

    ## create cyclic time features (to avoid discontinuities), add cols to date
    date["hour_sin"] = np.sin(2 * np.pi * hour / 24)
    date["hour_cos"] = np.cos(2 * np.pi * hour / 24)

    date["weekday_sin"] = np.sin(2 * np.pi * weekday / 7)
    date["weekday_cos"] = np.cos(2 * np.pi * weekday / 7)

    date["day_of_year_sin"] = np.sin(2 * np.pi * day_of_year / 365)
    date["day_of_year_cos"] = np.cos(2 * np.pi * day_of_year / 365)

    ## summarize time features
    X_time = date[
        [
            "hour_sin",
            "hour_cos",
            "weekday_sin",
            "weekday_cos",
            "day_of_year_sin",
            "day_of_year_cos",
        ]
    ].to_numpy(dtype=np.float32)

    ### Geo features
    station_ids = pd.read_csv(
        file_path, usecols=["station_uuid"], dtype={"station_uuid": "string"}
    )

    # Map UUIDs to coordinates
    coords = pd.read_csv(
        "training_data/station_uuid_to_coordinates.csv",
        usecols=["uuid", "latitude", "longitude"],
        dtype={"uuid": "string", "latitude": np.float32, "longitude": np.float32},
    )

    # load geo scaler parameters
    geo = np.load("geo_scaler.npz", allow_pickle=True)
    LAT_MEAN, LAT_STD = float(geo["lat_mean"]), float(geo["lat_std"])
    LON_MEAN, LON_STD = float(geo["lon_mean"]), float(geo["lon_std"])
    LAT_STD = max(LAT_STD, 1e-8)
    LON_STD = max(LON_STD, 1e-8)

    # UUIDs -> Coords (left join)
    station_coords = station_ids.merge(
        coords, left_on="station_uuid", right_on="uuid", how="left"
    )[["latitude", "longitude"]]

    # fill missing coords with mean values
    station_coords["latitude"] = station_coords["latitude"].fillna(LAT_MEAN)
    station_coords["longitude"] = station_coords["longitude"].fillna(LON_MEAN)

    # extract lat and lon as numpy arrays
    lat = station_coords["latitude"].to_numpy(dtype=np.float32)
    lon = station_coords["longitude"].to_numpy(dtype=np.float32)

    # normalize lat and lon
    lat = (lat - LAT_MEAN) / LAT_STD
    lon = (lon - LON_MEAN) / LON_STD

    ## combine features
    X_e5 = np.column_stack([X_time, lat, lon])
    X_e10 = np.column_stack([X_time, lat, lon])
    X_diesel = np.column_stack([X_time, lat, lon])

    ### make labels
    Y_e5 = pd.read_csv(file_path, usecols=["e5"]).to_numpy(dtype=np.float32)
    Y_e10 = pd.read_csv(file_path, usecols=["e10"]).to_numpy(dtype=np.float32)
    Y_diesel = pd.read_csv(file_path, usecols=["diesel"]).to_numpy(dtype=np.float32)

    ## remove rows with missing labels, reshape Ys
    mask = Y_e5 > 0
    X_e5 = X_e5[mask.flatten()]
    Y_e5 = Y_e5[mask]
    Y_e5 = Y_e5.reshape(-1, 1)

    mask = Y_e10 > 0
    X_e10 = X_e10[mask.flatten()]
    Y_e10 = Y_e10[mask]
    Y_e10 = Y_e10.reshape(-1, 1)

    mask = Y_diesel > 0
    X_diesel = X_diesel[mask.flatten()]
    Y_diesel = Y_diesel[mask]
    Y_diesel = Y_diesel.reshape(-1, 1)

    return X_e5, Y_e5, X_e10, Y_e10, X_diesel, Y_diesel


X_e5, Y_e5, X_e10, Y_e10, X_diesel, Y_diesel = get_data_chunk("2025", "09", "20")

# test training on 10 days with 1 day validation
# get validation data
X_val, Y_Val = None, None
# for day in range(1, 14 + 1):
#     print(f"Loading validation data for day 2025-10-{str(day).zfill(2)}")
#     X_e5_Val, Y_e5_Val, X_e10_Val, Y_e10_Val, X_diesel_Val, Y_diesel_Val = (
#         get_data_chunk("2025", "10", str(day).zfill(2))
#     )
#     X_val = np.concatenate([X_diesel_Val], axis=0)
#     Y_val = np.concatenate([Y_diesel_Val], axis=0)
# init models and trainers
MLP_diesel = MLP(n_features=X_e5.shape[1], output_size=1, n_hidden=2, hidden_size=16)
trainer = Trainer(MLP_diesel)

# MLP_diesel.load_weights("best_model_weights.npz")
# print(MLP_diesel.feed_forward(X_e5[:1]))
# print(Y_e5[:1])

# for i in range(2):  # number of training runs
#     for year in range(2024, 2025 + 1):
#         for month in range(1, 12 + 1):
#             for day in range(1, 31 + 1):
#                 # skip dates  with time changes
#                 if str(month).zfill(2) == "03" and (
#                     str(day).zfill(2) == "31" or str(day).zfill(2) == "30"
#                 ):
#                     continue

#                 print(
#                     f"Training on day {year}-{str(month).zfill(2)}-{str(day).zfill(2)} in run {i}."
#                 )

#                 # get data chunk
#                 try:
#                     X_e5, Y_e5, X_e10, Y_e10, X_diesel, Y_diesel = get_data_chunk(
#                         str(year), str(month).zfill(2), str(day).zfill(2)
#                     )
#                 except FileNotFoundError as e:
#                     print(
#                         f"Error loading data for day {year}-{str(month).zfill(2)}-{str(day).zfill(2)}: {e}"
#                     )
#                     continue

#                 if X_diesel is None or Y_diesel is None:
#                     print(
#                         f"Skipping day {year}-{str(month).zfill(2)}-{str(day).zfill(2)}"
#                     )
#                     continue

#                 # check for NaN or Inf values
#                 if not np.isfinite(X_diesel).all() or not np.isfinite(Y_diesel).all():
#                     print(
#                         "⚠️  Invalid value (NaN/Inf) in Batch. Skip this day.",
#                         f"X_bad={~np.isfinite(X_diesel).sum()}",
#                         f"Y_bad={~np.isfinite(Y_diesel).sum()}",
#                     )
#                     continue
#                 trainer.train(
#                     X_diesel,
#                     Y_diesel,
#                     X_val,
#                     Y_val,
#                     epochs=3,
#                     batch_size=512,
#                     patience=1,
#                 )

# test after training
print("Testing after training:")
MLP_diesel.load_weights("best_model_weights_diesel.npz")
for day in range(15, 25 + 1):
    print(f"Testing on day {day}.")
    X_e5, Y_e5, X_e10, Y_e10, X_diesel, Y_diesel = get_data_chunk(
        "2025", "10", str(day).zfill(2)
    )
    MLP_diesel_predictions = MLP_diesel.feed_forward(X_diesel)
    test_loss = np.mean((MLP_diesel_predictions - Y_diesel) ** 2)
    print(f"Test Loss on day {day}: {test_loss:.6f}")

# def __init__(self, n_features, output_size, n_hidden, hidden_size):
