import cupy as cp


def mse(y_true, y_pred):
    return cp.mean(cp.square(y_pred - y_true))


def mse_derivative(y_true, y_pred):
    n = y_true.shape[0]
    return (2 / n) * (y_pred - y_true)


class NeuronLayer:
    def __init__(self, input_size, output_size):
        # use He initialization for weights
        std = cp.sqrt(2.0 / input_size)
        # weights.shape = [n_inputs, n_neurons]
        self.weights = cp.random.normal(0, std, (input_size, output_size))
        # biases.shape = [1, n_neurons]
        self.biases = cp.zeros((1, output_size))

        # input_data.shape = [n_batch, n_inputs]
        self.input_data = None
        # z.shape=[n_batch, n_neurons]
        self.z = None

        self.delta_weights = None
        self.delta_biases = None

    def forward(self, input):
        self.input_data = input
        self.z = cp.dot(input, self.weights) + self.biases
        # use ReLU function
        return cp.max(0, self.z)

    def backward(self, output_gradient):
        # output_gradien.shape = [n_batch, n_neurons]

        # gradient ReLU: x > 0 = 1 else 0
        # relu_gradient.shape = [n_batch, n_neurons]
        relu_gradient = self.z > 0

        # delta.shape = [n_batch, n_neurons]
        delta = output_gradient * relu_gradient

        # [n_inputs, n_batch] @ [n_batch, n_neurons] = [n_inputs, n_neurons]
        self.delta_weights = cp.dot(self.input_data.T, delta)
        # [n_batch, n_neurons] -> [1, n_neurons]
        self.delta_biases = cp.sum(delta, axis=0, keepdims=True)

        # return gradient for next layer
        # [n_batch, n_inputs]
        return cp.dot(delta, self.weights.T)

    def update(self, learning_rate):
        self.weights = self.weights - learning_rate * self.delta_weights
        self.biases = self.biases - learning_rate * self.delta_biases
