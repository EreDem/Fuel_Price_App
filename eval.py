import cupy as cp
from mlp import MLP
from data_processing import DataLoader

#initialize MLP
mlp = MLP(7, 16, 2, 1)
mlp.load_weights()

# load eval data
X = DataLoader.load_data("insert file")
y = DataLoader.load_data("insert file")

def evaluate(mlp, X_test, y_test):
    y_pred = mlp.forward(X_test)
    
    mae = cp.mean(cp.abs(y_pred - y_test))
    
    print(f"MAE: {mae:.4f} Euro")


evaluate(mlp, X, y)