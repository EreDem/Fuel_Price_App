import numpy as np

from preprocessing import data_to_features


# Class for single layer of neurons
class neuron_layer:
    def __init__(self, n_features, n_neurons, leaky=True):
        self.leaky = leaky
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
        self.train_loss = 0
        # L2 regularization
        self.l2_lambda = 1e-4

        self.input_layer = neuron_layer(n_features, hidden_size)
        self.layers.append(self.input_layer)

        for i in range(n_hidden):
            self.layers.append(neuron_layer(hidden_size, hidden_size))

        self.output_layer = neuron_layer(hidden_size, output_size, False)
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
        self.train_loss = np.mean(error**2)

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

            learning_rate = 1e-3
            # update weights
            layer.weights -= learning_rate * dW
            layer.biases -= learning_rate * dB

            # L2 regularization
            layer.weights -= learning_rate * self.l2_lambda * layer.weights

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

    def train_on_data(
        self,
        batch_size: int = 512,
        training_on: str = "e5",
        epoch: int = 0,
    ):
        for year in range(2024, 2025 + 1):
            for month in range(1, 12 + 1):
                for day in range(1, 31 + 1):
                    # skip dates  with time changes
                    if str(month).zfill(2) == "03" and (
                        str(day).zfill(2) == "31" or str(day).zfill(2) == "30"
                    ):
                        continue

                    print(
                        f"Training on day {year}-{str(month).zfill(2)}-{str(day).zfill(2)} in {epoch}."
                    )

                    # get data chunk
                    try:
                        X_e5, Y_e5, X_e10, Y_e10, X_diesel, Y_diesel = data_to_features(
                            str(year), str(month).zfill(2), str(day).zfill(2)
                        )
                        fuel_map = {
                            "e5": (X_e5, Y_e5),
                            "e10": (X_e10, Y_e10),
                            "diesel": (X_diesel, Y_diesel),
                        }
                        X = fuel_map[training_on][0]
                        Y = fuel_map[training_on][1]
                    except FileNotFoundError as e:
                        print(
                            f"Error loading data for day {year}-{str(month).zfill(2)}-{str(day).zfill(2)}: {e}"
                        )
                        continue

                    if X is None or Y is None:
                        print(
                            f"Skipping day {year}-{str(month).zfill(2)}-{str(day).zfill(2)}"
                        )
                        continue

                    # check for NaN or Inf values
                    if not np.isfinite(X).all() or not np.isfinite(Y).all():
                        print(
                            "⚠️  Invalid value (NaN/Inf) in Batch. Skip this day.",
                            f"X_bad={~np.isfinite(X).sum()}",
                            f"Y_bad={~np.isfinite(Y).sum()}",
                        )
                        continue
                    for i in range(0, len(X), batch_size):
                        # split data in batches
                        X_batch = X[i : i + batch_size]
                        Y_batch = Y[i : i + batch_size]
                        # train on batch
                        self.model.backward(X_batch, Y_batch)
    
    def generate_validation_set(self, training_on: str = "diesel"):
        X_list = []
        Y_list = []

        for day in range(1, 14 + 1):
            day_str = str(day).zfill(2)
            print(f"Loading validation data for day 2025-10-{day_str}")
            try:
                (
                    X_e5_Val,
                    Y_e5_Val,
                    X_e10_Val,
                    Y_e10_Val,
                    X_diesel_Val,
                    Y_diesel_Val,
                ) = data_to_features("2025", "10", day_str)
            except FileNotFoundError:
                continue

            fuel_map = {
                "e5": (X_e5_Val, Y_e5_Val),
                "e10": (X_e10_Val, Y_e10_Val),
                "diesel": (X_diesel_Val, Y_diesel_Val),
            }
            Xv, Yv = fuel_map[training_on]

            if Xv is None or Yv is None:
                continue

            X_list.append(Xv)
            Y_list.append(Yv)

        if not X_list:
            raise RuntimeError("No validation data loaded.")

        X_val = np.concatenate(X_list, axis=0)
        Y_val = np.concatenate(Y_list, axis=0)
        return X_val, Y_val


    def train(self, epochs = 10, training_on = "e5", batch_size=512, patience=10):
        no_improve_epochs = 0
        best_loss = float("inf")
        best_params = None

        # get validation set
        X_val, Y_val = self.generate_validation_set(training_on=training_on)

        # training loop
        for epoch in range(epochs):
            # train on data
            self.train_on_data(batch_size=batch_size, training_on=training_on, epoch=epoch)
            ## validate after each epoch
            # calculate validation loss
            Y_val_pred = self.model.feed_forward(X_val)
            val_loss = np.mean((Y_val_pred - Y_val) ** 2)
            if np.isnan(val_loss):
                val_loss = np.inf

            print(
                f"Epoch {epoch + 1}/{epochs}, Train Error: {self.model.train_loss} Validation Loss: {val_loss:.6f}, no_improve_epochs: {no_improve_epochs}"
            )

            # early stopping check
            if val_loss < best_loss - 1e-4:
                best_loss = val_loss
                no_improve_epochs = 0
                # save best model weights
                best_params = self.model.get_params()
            else:
                no_improve_epochs += 1

            if best_params is None:
                best_params = self.model.get_params()

            if no_improve_epochs >= patience:
                self.model.set_params(best_params)
                self.model.save_weights(f"best_model_weights_{training_on}.npz")

                print(f"Early stopping at epoch {epoch + 1}")
                break

        # save best model weights in npz file
        self.model.set_params(best_params)
        self.model.save_weights(f"best_model_weights_{training_on}.npz")


