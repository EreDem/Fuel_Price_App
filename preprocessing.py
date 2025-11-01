import numpy as np
# from mlp import MLP
# from mlp import Trainer
import pandas as pd
import os


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

# We have to simulate the passing of time for the model to predict future prices
# Therefore we create new rows with the same base features but with a price from
# the future and a horizon feature indicating how far in the future the price is.
# This function adds a horizon feature to the csv file for a given date.
def add_horizon_to_csv(year: str, month: str, day: str):
    # load data from file
    file_path = f"training_data/{year}/{month}/{year}-{month}-{day}-prices.csv"
    
    # create temp directory for modified file
    temp_file_path = f"training_data/{year}/{month}/{year}-{month}-{day}-prices-temp.csv"

    # save data
    data = pd.read_csv(file_path)

    # write data into temp file


def data_to_features(year: str, month: str, day: str):
    # load data from file
    # file_path = f"training_data/{year}/{month}/{year}-{month}-{day}-prices.csv"
    file_path = f"training_example.csv"

    #### create features and labels

    ## brand one-hot features
    data = pd.read_csv(file_path)
    # sort by station and time
    data = data.sort_values(["station_uuid", "date"]).reset_index(drop=True)

    # map station_uuid to brand
    station_info = pd.read_csv(
        "stations.csv",   
        usecols=["uuid", "brand"]
    )

    print(data.columns)

    # merge brand into data
    data = data.merge(station_info, left_on="station_uuid", right_on="uuid", how="left")

    # missing brands to "Other"
    data["brand"] = data["brand"].fillna("Other")

    # fixed set of brands
    all_brands = ["Aral", "Esso", "Jet", "Total", "Shell", "Other"]

    # one-hot
    brand_dummies = pd.get_dummies(data["brand"], prefix="brand")

    # ensure all 6 columns exist
    expected_cols = [f"brand_{b}" for b in all_brands]
    brand_dummies = brand_dummies.reindex(columns=expected_cols, fill_value=0)

    # back to data
    data = pd.concat([data, brand_dummies], axis=1)

    # combine brand one hot features
    brand_features = data[[
        "brand_Aral",
        "brand_Esso",
        "brand_Jet",
        "brand_Total",
        "brand_Shell",
        "brand_Other"
    ]].to_numpy(dtype=np.float32)

    # get first col (date col) of csv
    date = pd.read_csv(
        file_path, usecols=["date"], parse_dates=["date"]
    )
    

    # time is given with time zone, which we do not need
    date["date"] = pd.to_datetime(date["date"], errors="coerce")
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

    
    isWeekend = (weekday == 5) | (weekday == 6)
    date["is_weekend"] = isWeekend.astype(np.float32)

    ## summarize time features
    X_time = date[
        [
            "hour_sin",
            "hour_cos",
            "weekday_sin",
            "weekday_cos",
            "day_of_year_sin",
            "day_of_year_cos",
            "is_weekend",
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

    ## raw oil price features
    # load oil prices
    oil_prices = pd.read_csv(
        "oil_prices.csv",
        usecols=["date", "brent_price"],
        parse_dates=["date"],
    )

    # create lag features
    oil_prices["oil_today"] = oil_prices["brent_price"]
    oil_prices["oil_yesterday"] = oil_prices["brent_price"].shift(1)
    oil_prices["oil_2days"] = oil_prices["brent_price"].shift(2)
    oil_prices["oil_3days"] = oil_prices["brent_price"].shift(3)
    oil_prices["oil_7days"] = oil_prices["brent_price"].shift(7)


    # drop rows with NaN (first 7 days)
    oil_prices = oil_prices.dropna().reset_index(drop=True)

    # extract oil features for the given date
    target_date = pd.Timestamp(f"{year}-{month}-{day}")

    # try exact match
    oil_row = oil_prices.loc[oil_prices["date"] == target_date]


    # extract values (shape (1,5))
    oil_vals = oil_row[
        ["oil_today", "oil_yesterday", "oil_2days", "oil_3days", "oil_7days"]
    ].to_numpy(dtype=np.float32).reshape(-1)

    n = len(X_time)   

    # Adjust shape
    oil_today_vec     = np.full(n, oil_vals[0], dtype=np.float32)
    oil_yesterday_vec = np.full(n, oil_vals[1], dtype=np.float32)
    oil_2days_vec     = np.full(n, oil_vals[2], dtype=np.float32)
    oil_3days_vec     = np.full(n, oil_vals[3], dtype=np.float32)
    oil_7days_vec     = np.full(n, oil_vals[4], dtype=np.float32)

    oil_features = np.column_stack([
        oil_today_vec,
        oil_yesterday_vec,
        oil_2days_vec,
        oil_3days_vec,
        oil_7days_vec,
    ])


    ## exchange rate features
    # load exchange rates
    exchange_rates = pd.read_csv(
        "exchange_rates.csv",
        usecols=["date", "eur_usd_rate"],
        parse_dates=["date"]
    )

    # drop rows with NaN (first 7 days)
    exchange_rates = exchange_rates.dropna().reset_index(drop=True)

    # create lag features
    exchange_rates["eur_usd_lag_1"] = exchange_rates["eur_usd_rate"].shift(1)
    exchange_rates["eur_usd_lag_7"] = exchange_rates["eur_usd_rate"].shift(7)
    exchange_rates["eur_usd_change_7d"] = exchange_rates["eur_usd_rate"].pct_change(7)

    # try exact match
    exchange_rates_row = exchange_rates.loc[exchange_rates["date"] == target_date]

    # extract values (shape (1,4))
    exchange_vals = exchange_rates_row[["eur_usd_rate", "eur_usd_lag_1", "eur_usd_lag_7", "eur_usd_change_7d"]].to_numpy(dtype=np.float32).reshape(-1)

    n = len(X_time)
    # Adjust shape
    eur_usd_rate_vec        = np.full(n, exchange_vals[0], dtype=np.float32)
    eur_usd_lag_1_vec      = np.full(n, exchange_vals[1], dtype=np.float32)
    eur_usd_lag_7_vec      = np.full(n, exchange_vals[2], dtype=np.float32)
    eur_usd_change_7d_vec  = np.full(n, exchange_vals[3], dtype=np.float32)

    # combine exchange rate features
    exchange_rates = np.column_stack([
        eur_usd_rate_vec,
        eur_usd_lag_1_vec,
        eur_usd_lag_7_vec,
        eur_usd_change_7d_vec,
    ])


    ## create price lag features
    # create last-price feature (previous entry for same station)
    for fuel in ["diesel", "e5", "e10"]:
        for lag in [1, 3, 10]:
            data[f"{fuel}_lag_{lag}"] = data.groupby("station_uuid")[fuel].shift(lag)

    lag_cols = [
        "diesel_lag_1", "diesel_lag_3", "diesel_lag_10",
        "e5_lag_1", "e5_lag_3", "e5_lag_10",
        "e10_lag_1", "e10_lag_3", "e10_lag_10",
    ]
    # drop rows where last price is missing (first entry per station)
    data = data.dropna(subset=lag_cols).reset_index(drop=True)

    # extract last price features
    X_last_diesel = data[["diesel_lag_1", "diesel_lag_3", "diesel_lag_10"]].to_numpy(dtype=np.float32)
    X_last_e5 = data[["e5_lag_1", "e5_lag_3", "e5_lag_10"]].to_numpy(dtype=np.float32)
    X_last_e10 = data[["e10_lag_1", "e10_lag_3", "e10_lag_10"]].to_numpy(dtype=np.float32)

    # test data shapes before combining
    print("X_time shape:", X_time.shape)
    print("lat shape:", lat.shape)
    print("lon shape:", lon.shape)
    print("oil_prices shape:", oil_features.shape)
    print("exchange_rates shape:", exchange_rates.shape)
    print("brand_features shape:", brand_features.shape)
    ## combine features
    X_e5 = np.column_stack([X_time, lat, lon, oil_features, exchange_rates, brand_features, X_last_e5])
    X_e10 = np.column_stack([X_time, lat, lon, oil_features, exchange_rates, brand_features, X_last_e10])
    X_diesel = np.column_stack([X_time, lat, lon, oil_features, exchange_rates, brand_features, X_last_diesel])

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

