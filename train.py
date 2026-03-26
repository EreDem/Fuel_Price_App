import cupy as cp
import numpy as np
from data_processing import DataLoader
from mlp import MLP, mse 

# initialize MLP with 7 input features, 2 hidden layers with 16 neurons each, and 1 output layer   
mlp = MLP(7, 16, 2, 1)

# Load training data
X = DataLoader.load_data("insert file")
y = DataLoader.load_data("insert file")

X_val = DataLoader.load_data("insert file")
y_val = DataLoader.load_data("insert file")

# training parameters
learning_rate = 0.001
batch_size = 1024
num_epochs = 100
val_counter = 0
patience = 3 
best_val_los = float("inf")

for epoch in range(num_epochs):
    # shuffle data set
    indices = np.random.permutation(len(X))
    X = X[indices]
    y = y[indices]

    for i in range(0, len(X), batch_size):
        X_batch = X[i : i + batch_size]
        y_batch = y[i : i + batch_size]

        y_pred = mlp.forward(X_batch)
        mlp.backward(y_batch, y_pred)
        mlp.update()
    
    # validate
    val_pred = mlp.forward(X_val)
    val_loss = mse(y_val, val_pred)
    
    if val_loss <= best_val_los : 
        best_val_los = val_loss
        val_counter = 0
        #save current best model
        mlp.save_weights()
    else: 
        val_counter += 1

    # early stopping
    if val_counter > patience: 
        break

    


