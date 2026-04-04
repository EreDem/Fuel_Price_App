from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from mlp import MLP
from data_processing import DataLoader, FeatureEngineer
import matplotlib.pyplot as plt


# initialize MLP
mlp = MLP(7, 16, 2, 1)
mlp.load_weights("model/weights/diesel")

# load eval data
X = DataLoader.load_data("training_data/training/eval_data/X_eval.csv")
y = DataLoader.load_data("training_data/training/eval_data/y_eval.csv")


def evaluate(mlp, X_test, y_test):
    y_pred = mlp.forward(X_test)

    mae = np.mean(np.abs(y_pred - y_test))

    print(f"MAE: {mae:.4f} Euro")


evaluate(mlp, X, y)
y_pred = mlp.forward(X)
print(y.max(), y.min())

plt.figure(figsize=(10, 6))
plt.scatter(y, y_pred, alpha=0.5)
plt.plot([y.min(), y.max()], [y.min(), y.max()], "r--", lw=2)
plt.xlabel("Actual Prices (Euro)")
plt.ylabel("Predicted Prices (Euro)")
plt.title("Model Predictions vs Actual Values")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# plot predictions for the next 24 hours
last_timestamp = datetime.strptime("2023-01-31 23:00:00", "%Y-%m-%d %H:%M:%S")
future_timestamps = [last_timestamp + timedelta(hours=i) for i in range(1, 25)]
future_features = FeatureEngineer.create_time_features(future_timestamps)
future_predictions = mlp.forward(future_features)
plt.figure(figsize=(12, 6))
plt.plot(future_timestamps, future_predictions.flatten(), marker="o")
plt.xlabel("Time")
plt.ylabel("Predicted Price (Euro)")
plt.title("Predicted Fuel Prices for the Next 24 Hours")
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
