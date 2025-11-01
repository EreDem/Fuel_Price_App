import pandas as pd
from mlp import MLP, Trainer
import numpy as np

# MLP_e5 = MLP(n_features=X_e5.shape[1], output_size=1, n_hidden=2, hidden_size=16)
# MLP_e5.load_weights("best_model_weights.npz")
# MLP_e5.feed_forward
stations = pd.read_csv(
    "stations.csv", usecols=["uuid", "latitude", "longitude"]
).drop_duplicates()
stations = stations.sort_values("uuid").reset_index(drop=True)
stations[["uuid", "latitude", "longitude"]].to_csv(
    "station_uuid_to_coordinates.csv", index=False
)

# Eingabe- und Ausgabedateien
# INPUT_FILE = "stations.csv"
# OUTPUT_FILE = "stations.json"

# # CSV einlesen
# df = pd.read_csv(
#     INPUT_FILE,
#     usecols=["uuid", "brand", "street", "house_number", "post_code", "city"],
#     dtype=str  # alles als String, damit z. B. Postleitzahlen führende Nullen behalten
# )

# # Spalten ggf. umbenennen (optional)
# df = df.rename(columns={
#     "uuid": "id",
#     "brand": "brand",
#     "street": "street",
#     "house_number": "house_number",
#     "post_code": "zip",
#     "city": "city",
# })

# # Als JSON exportieren (Liste von Objekten)
# df.to_json(OUTPUT_FILE, orient="records", force_ascii=False, indent=2)

# print(f"{len(df)} Einträge in '{OUTPUT_FILE}' gespeichert.")
