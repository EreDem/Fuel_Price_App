import pandas as pd
from mlp import MLP, Trainer
import numpy as np

MLP_e5 = MLP(n_features=X_e5.shape[1], output_size=1, n_hidden=2, hidden_size=16)
MLP_e5.load_weights("best_model_weights.npz")
MLP_e5.feed_forward
# stations = pd.read_csv(
#     "training_data/stations.csv", usecols=["uuid", "latitude", "longitude"]
# ).drop_duplicates()
# stations = stations.sort_values("uuid").reset_index(drop=True)
# stations[["uuid", "latitude", "longitude"]].to_csv(
#     "training_data/station_uuid_to_coordinates.csv", index=False
# )
