import numpy as np


def mse(y_true, y_pred):
    return np.mean(np.square(y_pred - y_true))


def mse_derivative(y_true, y_pred):
    n = y_true.shape[0]
    return (2 / n) * (y_pred - y_true)


class NeuronLayer:
    def __init__(self, input_size, output_size):
        # use He initialization for weights
        std = np.sqrt(2.0 / input_size)
        # weights.shape = [n_inputs, n_neurons]
        self.weights = np.random.normal(0, std, (input_size, output_size))
        # biases.shape = [1, n_neurons]
        self.biases = np.zeros((1, output_size))

        # input_data.shape = [n_batch, n_inputs]
        self.input_data = None
        # z.shape=[n_batch, n_neurons]
        self.z = None

        self.delta_weights = None
        self.delta_biases = None

    def forward(self, input):
        self.input_data = input
        self.z = np.dot(input, self.weights) + self.biases
        # use ReLU function
        return np.maximum(0, self.z)

    def backward(self, output_gradient):
        # output_gradien.shape = [n_batch, n_neurons]

        # gradient ReLU: x > 0 = 1 else 0
        # relu_gradient.shape = [n_batch, n_neurons]
        relu_gradient = self.z > 0

        # delta.shape = [n_batch, n_neurons]
        delta = output_gradient * relu_gradient

        # [n_inputs, n_batch] @ [n_batch, n_neurons] = [n_inputs, n_neurons]
        self.delta_weights = np.dot(self.input_data.T, delta)
        # [n_batch, n_neurons] -> [1, n_neurons]
        self.delta_biases = np.sum(delta, axis=0, keepdims=True)

        # return gradient for next layer
        # [n_batch, n_inputs]
        return np.dot(delta, self.weights.T)

    def update(self, learning_rate):
        self.weights = self.weights - learning_rate * self.delta_weights
        self.biases = self.biases - learning_rate * self.delta_biases


class MLP:
    def __init__(
        self, input_layer_size, layer_sizes, number_hidden_layers, output_layer_size
    ):
        self.layers = []
        self.layers.append(NeuronLayer(input_layer_size, layer_sizes))
        for i in range(number_hidden_layers - 1):
            self.layers.append(NeuronLayer(layer_sizes, layer_sizes))
        self.layers.append(NeuronLayer(layer_sizes, output_layer_size))

    def forward(self, X):
        output = X
        for layer in self.layers:
            output = layer.forward(output)
        return output

    def backward(self, y_true, y_pred):
        # compute gradient of loss with respect to output
        output_gradient = mse_derivative(y_true, y_pred)
        # backpropagate through layers in reverse order
        for layer in reversed(self.layers):
            output_gradient = layer.backward(output_gradient)

    def update(self, learning_rate):
        for layer in self.layers:
            layer.update(learning_rate)

    def save_weights(self):
        # save weights and biases to file
        for i, layer in enumerate(self.layers):
            np.save(f"layer_{i}_weights.npy", layer.weights)
            np.save(f"layer_{i}_biases.npy", layer.biases)

    def load_weights(self):
        # load weights and biases from file
        for i, layer in enumerate(self.layers):
            layer.weights = np.load(f"layer_{i}_weights.npy")
            layer.biases = np.load(f"layer_{i}_biases.npy")

    def predict(self, X):
        return self.forward(X)
