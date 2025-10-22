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

    def train(self, X, Y, iterations):
        for i in range(iterations):
            self.backward(X, Y)

 
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

# test mlp
MLP = MLP(1, 1, 2, 4)
X = np.array([[0], [1], [2], [3], [4]])
Y = np.array([[0], [3], [6], [9], [12]])
X_test = np.array([[15]])
MLP.load_weights("trained_weights.npz")
print(MLP.feed_forward(X_test))