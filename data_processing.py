# This file creates features from the raw data

# List of available raw data:
# date-type-data: 
# - day_of_week
# - is_weekend
# - time 
# - month and larger time periods would only be useful if we had long term data, which we don't have
# location-type-data:
# - latitude
# - longitude
# - size of the area (if available)
# - highway or not (if available)
# external factors:
# - raw oil price 
# - Euro-Dollar exchange rate
# - price lag features
# - brand of gas station

# Feature engineering ideas:
# - date-type features will be cyclic features
# - we will use the coordinates to determine wether the gas station is in a city or on a highway, and we can also use the coordinates to determine the average price in the area, which can be a useful feature.
# - we will normalize the oil price and exchange rate using z-score
# - we can create lag features for the price, oil price and exchange rate

# The Data
# The data is in a csv file. We will read the data using pandas.
# The data has the following columns:
# date, station_uuid, diesel, e5, e10, dieselchange, e5change, e10change

import pandas as pd
import numpy as np

class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self, columns=None):
        data = pd.read_csv(self.file_path)
        return data
    
class Normalizer:
    def __init__(self):
        pass

    # normalize using z-score
    def normalize_price(self, column):
        mean = np.mean(column)
        std = np.std(column)
        return (column - mean) / std
    
    # convert hours into minutes to create a continuous feature
    def normalize_time(self, hours_column, minutes_column):
        time_column = (hours_column * 60) + minutes_column
        return time_column

    
class FeatureEngineer:
    def __init__(self, data: np.array):
        self.data = data
    # Format of data matrix:
    # [date],[station_uuid],[diesel],[e5],[e10],[dieselchange],[e5change],[e10change]

    #Format of feature matrix:
    # [time_sin],[time_cos],[day_sin],[day_cos],[is_weekend],[is_holiday],[is_day_before_holiday],[price_lag_1h],[price_lag_24h],[price_mean_24h],[price_diff_3h],[oil_price_1d],[oil_price_3d],[exchange_rate],[brand_one_hot]

    def create_time_features(self, date_column):

        date_column = pd.to_datetime(date_column)

        hours_column = date_column.hour
        minutes_column = date_column.minute
        time_column = Normalizer.normalize_time(hours_column, minutes_column)

        time_sin = np.sin(2 * np.pi * time_column / (24 * 60))
        time_cos = np.cos(2 * np.pi * time_column / (24 * 60))

        day_of_week_column = date_column.dayofweek

        day_sin = np.sin(2 * np.pi * day_of_week_column / 7)
        day_cos = np.cos(2 * np.pi * day_of_week_column / 7)
        
        is_weekend = date_column.dt.dayofweek >= 5

        # set of german holidays in 2026
        holidays = ['2026-01-01', '2026-02-11', '2026-02-12', '2026-02-13', '2026-02-14', '2026-02-15', '2026-03-17', '2026-04-06', '2026-05-01', '2026-06-14', '2026-09-29', '2026-10-01', '2026-10-02', '2026-10-03', '2026-10-04', '2026-10-05', '2026-11-02', '2026-12-25']
        holidays = pd.to_datetime(holidays)

        is_holiday = date_column.isin(holidays)
        is_day_before_holiday = date_column.isin(holidays - pd.Timedelta(days=1))

        time_features = [time_sin, time_cos, day_sin, day_cos, is_weekend, is_holiday, is_day_before_holiday]
        return time_features
    
    def create_brand_one_hot(self, station_uuid_column):
        # we will create a one-hot encoding for the brand of the gas station, which is determined by the station_uuid
        # we will do a lookup for the uuid in a different file that contains the mapping of uuid to brand
        brands = {"Aral": 0, "Jet": 1, "Shell": 2, "Total": 3, "Esso": 4, "Bft": 5}
        
        uuid_df = pd.read_csv("uuid_to_brand.csv")
        mapping_dict = dict(zip(uuid_df["id"], uuid_df["brand"]))

        # generate one-hot encoding for the brands
        brand_one_hot = np.zeros((len(station_uuid_column), len(brands)+1))

        for index in range(len(station_uuid_column)):
            uuid = station_uuid_column[index]
            brand = mapping_dict.get(uuid, "Other")
            brand_index = brands.get(brand, len(brands)) # if the brand is not in the list, we will assign it to "other"
            brand_one_hot[index, brand_index] = 1

        return brand_one_hot

    def assemble_matrix(self, *columns):
        feature_matrix = []
        for column in columns:
            feature_matrix.append(column)
        return np.array(feature_matrix).T
    
    def create_feature_matrix(self):
        return self.assemble_matrix(self.create_time_features(self.data[:, 0]), self.create_brand_one_hot(self.data[:, 1]))