import pandas as pd

stations = pd.read_csv("training_data/stations.csv", usecols=["uuid", "latitude", "longitude"]).drop_duplicates()
stations = stations.sort_values("uuid").reset_index(drop=True)
stations[["uuid", "latitude", "longitude"]].to_csv("training_data/station_uuid_to_coordinates.csv", index=False)

