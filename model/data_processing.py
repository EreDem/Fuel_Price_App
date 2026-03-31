# This file creates features from the raw data

import pandas as pd
import numpy as np
import numpy as np
import os


class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    @staticmethod
    def load_data(file_path, rows=None, columns=None):
        data = pd.read_csv(file_path)
        if rows is not None:
            data = data.iloc[rows]
        if columns is not None:
            data = data.iloc[:, columns]
        return data

    @staticmethod
    def save_data(data: np.array, destination):
        pd.DataFrame(data).to_csv(destination, index=False)

    @staticmethod
    def clean_data(data):
        # remove rows with missing values
        data = data.dropna()
        data = data.values
        # remove outliers with 3-sigma rule for the price columns (diesel, e5, e10)
        for col in [2, 3, 4]:  # price columns are at index 2, 3, 4
            mean = np.mean(data[:, col])
            std = np.std(data[:, col])
            sigma = 0.5
            data = data[
                (data[:, col] >= mean - sigma * std)
                & (data[:, col] <= mean + sigma * std)
            ]
        # remove rows with prices equal to 0
        data = data[(data[:, 2] != 0) & (data[:, 3] != 0) & (data[:, 4] != 0)]
        return data


class Normalizer:
    def __init__(self):
        pass

    # normalize using z-score
    @staticmethod
    def normalize_price(column):
        mean = np.mean(column)
        std = np.std(column)
        return (column - mean) / std

    # convert hours into minutes to create a continuous feature
    @staticmethod
    def normalize_time(hours_column, minutes_column):
        time_column = (hours_column * 60) + minutes_column
        return time_column


class FeatureEngineer:
    def __init__(self, data):
        self.data = data

    # Format of data matrix:
    # [date],[station_uuid],[diesel],[e5],[e10],[dieselchange],[e5change],[e10change]

    # Format of feature matrix:
    # [time_sin],[time_cos],[day_sin],[day_cos],[is_weekend],[is_holiday],[is_day_before_holiday],[price_lag_1h],[price_lag_24h],[price_min_24h],[price_diff_3h],[oil_price_1d],[oil_price_3d],[exchange_rate],[brand_one_hot]

    @staticmethod
    def extract_labels(data, *col):
        # we will predict the e5 price, which is at index 3
        labels = data[:, col]
        return labels

    @staticmethod
    def create_time_features(date_column):

        date_column = pd.to_datetime(date_column)

        hours_column = date_column.hour
        minutes_column = date_column.minute
        time_column = Normalizer.normalize_time(hours_column, minutes_column)

        time_sin = np.sin(2 * np.pi * time_column / (24 * 60))
        time_cos = np.cos(2 * np.pi * time_column / (24 * 60))

        day_of_week_column = date_column.dayofweek

        day_sin = np.sin(2 * np.pi * day_of_week_column / 7)
        day_cos = np.cos(2 * np.pi * day_of_week_column / 7)

        is_weekend = day_of_week_column >= 5

        # german holidays in 2026
        holidays = [
            "2026-01-01",
            "2026-02-11",
            "2026-02-12",
            "2026-02-13",
            "2026-02-14",
            "2026-02-15",
            "2026-03-17",
            "2026-04-06",
            "2026-05-01",
            "2026-06-14",
            "2026-09-29",
            "2026-10-01",
            "2026-10-02",
            "2026-10-03",
            "2026-10-04",
            "2026-10-05",
            "2026-11-02",
            "2026-12-25",
        ]
        holidays = pd.to_datetime(holidays)

        is_holiday = date_column.isin(holidays)
        is_day_before_holiday = date_column.isin(holidays - pd.Timedelta(days=1))

        time_features = np.column_stack(
            (
                time_sin,
                time_cos,
                day_sin,
                day_cos,
                is_weekend,
                is_holiday,
                is_day_before_holiday,
            )
        )
        # shape [data, 7]
        return time_features

    def create_price_lag_features(self, lag_hours):
        timestamps = pd.to_datetime(self.data[:, 0]).floor(
            "h"
        )  # round down to the nearest hour to get one price per hour
        uuids = self.data[:, 1]
        prices = self.data[:, 3]  # e5 price is at index 3

        price_lookup = {
            (uuid, time): price for uuid, time, price in zip(uuids, timestamps, prices)
        }

        time_delta = pd.Timedelta(hours=lag_hours)

        price_lag_column = np.zeros(len(self.data))

        for i in range(len(self.data)):
            target_time = timestamps[i] - time_delta
            current_uuid = uuids[i]
            price_lag_column[i] = price_lookup.get(
                (current_uuid, target_time), prices[i]
            )

        # shape [data, 1]
        return price_lag_column

    def create_price_min_24h_features(self):
        timestamps = pd.to_datetime(self.data[:, 0]).floor(
            "h"
        )  # round down to the nearest hour to get one price per hour
        uuids = self.data[:, 1]
        prices = self.data[:, 3]  # e5 price is at index 3

        price_lookup = {
            (uuid, time): price for uuid, time, price in zip(uuids, timestamps, prices)
        }

        price_min_24h_column = np.zeros(len(self.data))

        for i in range(len(self.data)):
            current_uuid = uuids[i]
            current_time = timestamps[i]
            past_24h_times = [
                current_time - pd.Timedelta(hours=h) for h in range(1, 25)
            ]
            past_24h_prices = [
                price_lookup.get((current_uuid, time), prices[i])
                for time in past_24h_times
            ]
            price_min_24h_column[i] = min(past_24h_prices)

        # shape [data, 1]
        return price_min_24h_column

    def create_brand_one_hot(self, station_uuid_column):
        # we will create a one-hot encoding for the brand of the gas station, which is determined by the station_uuid
        # we will do a lookup for the uuid in a different file that contains the mapping of uuid to brand
        brands = {"Aral": 0, "Jet": 1, "Shell": 2, "Total": 3, "Esso": 4, "Bft": 5}

        uuid_df = pd.read_csv("uuid_to_brand.csv")
        mapping_dict = dict(zip(uuid_df["id"], uuid_df["brand"]))

        # generate one-hot encoding for the brands
        brand_one_hot = np.zeros((len(station_uuid_column), len(brands) + 1))

        for index in range(len(station_uuid_column)):
            uuid = station_uuid_column[index]
            brand = mapping_dict.get(uuid, "Other")
            brand_index = brands.get(
                brand, len(brands)
            )  # if the brand is not in the list, we will assign it to "other"
            brand_one_hot[index, brand_index] = 1
        # shape [data, 6]
        return brand_one_hot

    @staticmethod
    def assemble_matrix(*columns):
        return np.column_stack(columns)

    @staticmethod
    def create_feature_matrix(data):
        # shape [data, 7 + 1 + 1 + 1 + 6] = [data, 16] , add self.create_brand_one_hot(self.data[:, 1]), self.create_price_lag_features(24), self.create_price_min_24h_features(), , self.create_price_lag_features(1)
        return FeatureEngineer.assemble_matrix(
            FeatureEngineer.create_time_features(data[:, 0])
        )


if __name__ == "__main__":
    # workflow
    # create X and y
    # START LOOP
    # create variables features and labels
    # get data day batch
    # clean batch
    # extract labels
    #   - save in labels
    # create features
    #   - save in features
    # stack features to X and labels to y
    # END LOOP
    # shuffle X und y
    # save X and y

    # create training features and labels
    X = []
    y = []

    raw_data_dir = "training_data/raw_data"
    destination_dir = "training_data/training/train_data/features_lables"

    # the raw training data is stored  in "training_data/raw_data", they are ordered by days
    for day in os.listdir(raw_data_dir):
        data = DataLoader.load_data(os.path.join(raw_data_dir, day))
        clean_data = DataLoader.clean_data(data)
        labels = FeatureEngineer.extract_labels(clean_data, 3)
        features = FeatureEngineer.create_feature_matrix(clean_data)
        X.append(features)
        y.append(labels)

    # shuffle data set
    indices = np.random.permutation(len(X))
    # X and y are lists at this point; use numpy indexing after converting to array
    X = np.array(X, dtype=object)[indices]
    y = np.array(y, dtype=object)[indices]

    X = np.vstack(X).astype(np.float32)
    y = np.vstack(y).astype(np.float32)

    DataLoader.save_data(X, "training_data/training/train_data/features_lables/X.csv")
    DataLoader.save_data(y, "training_data/training/train_data/features_lables/y.csv")

    # create validation features and labels
    X_val = []
    y_val = []

    raw_data_dir = "training_data/raw_data"
    destination_dir = "training_data/training/train_data/features_lables"

    # the raw training data is stored  in "training_data/raw_data", they are ordered by days
    # for day in os.listdir(raw_data_dir):
    # data = DataLoader.load_data(os.path.join(raw_data_dir, day))
    data = DataLoader.load_data("training_data/raw_data/2026-03-21-prices.csv")
    clean_data = DataLoader.clean_data(data)
    labels = FeatureEngineer.extract_labels(clean_data, 3)
    features = FeatureEngineer.create_feature_matrix(clean_data)
    X_val.append(features)
    y_val.append(labels)

    # shuffle data set
    indices = np.random.permutation(len(X_val))
    # X and y are lists at this point; use numpy indexing after converting to array
    X_val = np.array(X_val, dtype=object)[indices]
    y_val = np.array(y_val, dtype=object)[indices]

    X_val = np.vstack(X_val).astype(np.float32)
    y_val = np.vstack(y_val).astype(np.float32)

    DataLoader.save_data(X_val, "training_data/training/val_data/X_val.csv")
    DataLoader.save_data(y_val, "training_data/training/val_data/y_val.csv")

    # create eval features and labels
    X_eval = []
    y_eval = []

    raw_data_dir = "training_data/raw_data"
    destination_dir = "training_data/training/train_data/features_lables"

    # the raw training data is stored  in "training_data/raw_data", they are ordered by days
    # for day in os.listdir(raw_data_dir):
    # data = DataLoader.load_data(os.path.join(raw_data_dir, day))
    data = DataLoader.load_data("training_data/raw_data/2026-03-22-prices.csv")
    clean_data = DataLoader.clean_data(data)
    labels = FeatureEngineer.extract_labels(clean_data, 3)
    features = FeatureEngineer.create_feature_matrix(clean_data)
    X_eval.append(features)
    y_eval.append(labels)

    # shuffle data set
    indices = np.random.permutation(len(X_eval))
    # X and y are lists at this point; use numpy indexing after converting to array
    X_eval = np.array(X_eval, dtype=object)[indices]
    y_eval = np.array(y_eval, dtype=object)[indices]

    X_eval = np.vstack(X_eval).astype(np.float32)
    y_eval = np.vstack(y_eval).astype(np.float32)

    DataLoader.save_data(X_eval, "training_data/training/eval_data/X_eval.csv")
    DataLoader.save_data(y_eval, "training_data/training/eval_data/y_eval.csv")
