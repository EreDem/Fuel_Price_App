import numpy as np
from mlp import MLP
import pandas as pd

train_data_folder = "training_data"
training_year_data_files = ["/2024", "/2025"] 
months = ["/01", "/02", "/03", "/04", "/05", "/06", "/07", "/08", "/09", "/10", "/11", "/12"] 

# get data chunk and preprocess
def get_data_chunk(year: str, month: str, day: str):
    # load data from file
    file_path = f"training_data/{year}/{month}/{year}-{month}-{day}-prices.csv"

    #### create features and labels

    ## date features
    # get first col (date col) of csv
    date = pd.read_csv(file_path, usecols=["date"], parse_dates=[0])

    # time is given with time zone, which we do not need
    date["date"] = date["date"].dt.tz_localize(None)

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
    X_time = date[[
    "hour_sin", "hour_cos",
    "weekday_sin", "weekday_cos",
    "day_of_year_sin", "day_of_year_cos"
    ]].to_numpy(dtype=np.float32)

    ### Geo features
    station_ids = pd.read_csv(file_path, usecols=["station_uuid"], dtype={"station_uuid": "string"})

    # convert uuids to coordinates
    coords = pd.read_csv("training_data/station_uuid_to_coordinates.csv", usecols=["uuid", "latitude", "longitude"], dtype={"uuid": "string", "latitude": np.float32, "longitude": np.float32})

    station_coords = station_ids.merge(coords, left_on="station_uuid", right_on="uuid", how="left")[["latitude", "longitude"]]

    lat = station_coords["latitude"].to_numpy(dtype=np.float32)
    lon = station_coords["longitude"].to_numpy(dtype=np.float32)

    # get mean and std for normalization
    lat_mean, lat_std = lat.mean(), lat.std()
    lon_mean, lon_std = lon.mean(), lon.std()

    # normalize
    lat = (lat - lat_mean) / lat_std
    lon = (lon - lon_mean) / lon_std

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


X_e5, Y_e5, X_e10, Y_e10, X_diesel, Y_diesel = get_data_chunk("2025", "06", "01")

MLP_e5 = MLP(n_features=X_e5.shape[1], output_size=1, n_hidden=2, hidden_size=16)
MLP_e5.train(X_e5, Y_e5, iterations=1)
print(X_e5[0])
print(MLP_e5.feed_forward(X_e5[0]))

    # def __init__(self, n_features, output_size, n_hidden, hidden_size):