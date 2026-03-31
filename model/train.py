import numpy as np
from data_processing import DataLoader
from model.mlp import MLP, mse

# initialize MLP with 7 input features, 2 hidden layers with 16 neurons each, and 1 output layer
print("initializing mlp...")
mlp = MLP(7, 16, 2, 1)

# Load training data
print("Loading X...")
X = DataLoader.load_data("training_data/training/train_data/features_lables/X.csv")
print("Loading y...")
y = DataLoader.load_data("training_data/training/train_data/features_lables/y.csv")

print("Loading X_val...")
X_val = DataLoader.load_data("training_data/training/val_data/X_val.csv")
print("Loading y_val...")
y_val = DataLoader.load_data("training_data/training/val_data/y_val.csv")

# move arrays to GPU if available; otherwise use NumPy arrays
X = np.asarray(X)
y = np.asarray(y)
X_val = np.asarray(X_val)
y_val = np.asarray(y_val)

# training parameters
learning_rate = 0.001
batch_size = 1024
num_epochs = 100
val_counter = 0
patience = 3
best_val_los = float("inf")

print("starting training...")
for epoch in range(num_epochs):
    print(f"Training in epoch {epoch}")
    # shuffle data set
    indices = np.random.permutation(len(X))
    X = X[indices]
    y = y[indices]

    for i in range(0, len(X), batch_size):
        X_batch = X[i : i + batch_size]
        y_batch = y[i : i + batch_size]

        y_pred = mlp.forward(X_batch)
        mlp.backward(y_batch, y_pred)
        mlp.update(learning_rate)

    print("current epoch training loss:", mse(y_batch, y_pred))
    print("current epoch validation loss:", mse(y_val, mlp.forward(X_val)))

    # validate
    val_pred = mlp.forward(X_val)
    val_loss = mse(y_val, val_pred)

    if val_loss <= best_val_los:
        best_val_los = val_loss
        val_counter = 0
        # save current best model
        mlp.save_weights()
    else:
        val_counter += 1

    # early stopping
    if val_counter > patience:
        break
