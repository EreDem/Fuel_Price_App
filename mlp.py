import numpy as np

# Class for single layer of neurons
class neuron_layer:
    def __init__(self, n_features, n_neurons):
        # use he normal initialization to avoid a dead network
        self.weights = np.random.randn(n_features, n_neurons) * np.sqrt(
            2.0 / n_features
        )
        # initialize biases as not zeros for same reason
        self.biases = np.full((1, n_neurons), 0.01)

    # leaky relu instead of relu for same reason
    def leaky_relu(self, x):
        return np.where(x > 0, x, 0.01 * x)

    def forward(self, X):
        self.Z = np.dot(X, self.weights) + self.biases
        self.A = self.leaky_relu(self.Z)
        return self.A


class MLP:
    def __init__(self, n_features, output_size, n_hidden, hidden_size):
        # create all layers and safe in list
        self.layers = []

        self.input_layer = neuron_layer(n_features, hidden_size)
        self.layers.append(self.input_layer)

        for i in range(n_hidden):
            self.layers.append(neuron_layer(hidden_size, hidden_size))

        self.output_layer = neuron_layer(hidden_size, output_size)
        self.layers.append(self.output_layer)

    def get_params(self):
        params = []
        for layer in self.layers:
            params.append((layer.weights.copy(), layer.biases.copy()))
        return params
    
    def set_params(self, params):
        for layer, (W, b) in zip(self.layers, params):
            layer.weights[...] = W
            layer.biases[...] = b

    def feed_forward(self, X):
        A = X
        for layer in self.layers:
            A = layer.forward(A)
        return A

    def leaky_relu_deriv(self, x):
        return np.where(x > 0, 1.0, 0.01)

    def backward(self, X, Y):
        # determine prediction and error
        Y_pred = self.feed_forward(X)
        error = Y_pred - Y

        # get number of samples to normalize
        m = X.shape[0]

        # calculate delta for output layer
        delta = error * self.leaky_relu_deriv(self.layers[-1].Z)

        for l in reversed(range(len(self.layers))):
            layer = self.layers[l]
            # first layer has A = Input
            A_prev = X if l == 0 else self.layers[l - 1].A

            # calculate gradients
            dW = np.dot(A_prev.T, delta) / m  # normalize over m samples
            dB = np.sum(delta, axis=0, keepdims=True) / m  # normalize over m samples

            # set delta to previous delta
            if l > 0:
                delta = np.dot(delta, layer.weights.T) * self.leaky_relu_deriv(
                    self.layers[l - 1].Z
                )

            learning_rate = 0.01
            # update weights
            layer.weights -= learning_rate * dW
            layer.biases -= learning_rate * dB

 
    # safe and load weights in different file
    def save_weights(self, path: str):
        arrays = {}
        for i, layer in enumerate(self.layers):
            arrays[f"W{i}"] = layer.weights
            arrays[f"b{i}"] = layer.biases
        np.savez_compressed(path, **arrays)

    def load_weights(self, path: str):
        data = np.load(path, allow_pickle=False)
        for i, layer in enumerate(self.layers):
            W = data[f"W{i}"]
            b = data[f"b{i}"]
            # Check shapes of weights and biases
            assert (
                layer.weights.shape == W.shape and layer.biases.shape == b.shape
            ), f"Shape mismatch at layer {i}: got {W.shape}/{b.shape}, expected {layer.weights.shape}/{layer.biases.shape}"
            layer.weights[...] = W
            layer.biases[...] = b


class Trainer:
    def __init__(self, model: MLP):
        self.model = model

    def train_on_batch(self, X_batch, Y_batch, ):
            self.model.backward(X_batch, Y_batch)

    def train(self, X, Y, X_val, Y_val, epochs, batch_size=32, patience=10):
        no_improve_epochs = 0
        best_loss = float('inf')
        best_params = None

        for epoch in range(epochs):
            for i in range(0, len(X), batch_size):
                # split data in batches
                X_batch = X[i:i + batch_size]
                Y_batch = Y[i:i + batch_size]
                # train on batch
                self.train_on_batch(X_batch, Y_batch)
            ## validate after each epoch
            # calculate validation loss
            Y_val_pred = self.model.feed_forward(X_val)
            val_loss = np.mean((Y_val_pred - Y_val) ** 2)

            # early stopping check
            if val_loss < best_loss - 1e-4:
                best_loss = val_loss
                no_improve_epochs = 0
                # save best model weights
                best_params = self.model.get_params()
            else:
                no_improve_epochs += 1

            if no_improve_epochs >= patience:
                self.model.set_params(best_params)
                self.model.save_weights("best_model_weights.npz")

                print(f"Early stopping at epoch {epoch + 1}")
                break

        # save best model weights in npz file
        self.model.set_params(best_params)
        self.model.save_weights("best_model_weights.npz")

# test mlp
# MLP = MLP(1, 1, 2, 4)
# X = np.array([[0], [1], [2], [3], [4]])
# Y = np.array([[0], [3], [6], [9], [12]])
# X_test = np.array([[15]])
# MLP.train(X, Y, 10000)
# MLP.save_weights("trained_weights.npz")
# print(MLP.feed_forward(X_test))