import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import matplotlib.pyplot as plt
import os

# Disable GPU
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# Load MNIST dataset
(x_train, _), (x_test, _) = keras.datasets.mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0  # Normalize to [0,1]

# Flatten images (28x28 -> 784)
x_train = x_train.reshape(-1, 784)
x_test = x_test.reshape(-1, 784)


class SparseAutoencoder(keras.Model):
    def __init__(self, encoding_dim=32):
        super(SparseAutoencoder, self).__init__()

        # Encoder
        self.encoder = keras.Sequential(
            [
                layers.Dense(128, activation=layers.LeakyReLU(alpha=0.1)),
                layers.BatchNormalization(),
                layers.Dropout(0.2),
                layers.Dense(encoding_dim, activation="sigmoid"),
            ]
        )

        # Decoder
        self.decoder = keras.Sequential(
            [
                layers.Dense(128, activation=layers.LeakyReLU(alpha=0.1)),
                layers.BatchNormalization(),
                layers.Dropout(0.2),
                layers.Dense(784, activation="sigmoid"),
            ]
        )

    def call(self, inputs):
        encoded = self.encoder(inputs)
        decoded = self.decoder(encoded)
        return decoded

    def compute_sparsity_loss(self, encoded):
        sparsity_level = 0.05
        beta = 1
        rho_hat = tf.reduce_mean(encoded, axis=0)  # Average activation per neuron
        kl_div = sparsity_level * tf.math.log(sparsity_level / rho_hat) + (
                1 - sparsity_level
        ) * tf.math.log((1 - sparsity_level) / (1 - rho_hat))
        return beta * tf.reduce_sum(kl_div)


# Create model
autoencoder = SparseAutoencoder(encoding_dim=32)

# Compile model with custom loss function
optimizer = keras.optimizers.Adam(learning_rate=0.001)


def custom_loss(y_true, y_pred):
    reconstruction_loss = keras.losses.mean_squared_error(y_true, y_pred)
    sparsity_loss = autoencoder.compute_sparsity_loss(autoencoder.encoder(y_true))
    return reconstruction_loss + sparsity_loss


autoencoder.compile(optimizer=optimizer, loss=custom_loss)

# Learning rate scheduler callback
lr_scheduler = keras.callbacks.LearningRateScheduler(lambda epoch: 0.001 * (1 + np.cos(np.pi * epoch / 10)) / 2)

# Train autoencoder
history = autoencoder.fit(
    x_train,
    x_train,
    epochs=10,
    batch_size=256,
    validation_data=(x_test, x_test),
    callbacks=[lr_scheduler],
)

# Clear previous models from memory
tf.keras.backend.clear_session()


# Visualizing reconstructed images
def visualize_reconstruction(model, images, n=20):
    decoded_imgs = model.predict(images[:n])
    plt.figure(figsize=(40, 4))
    for i in range(n):
        # Original images
        plt.subplot(2, n, i + 1)
        plt.imshow(images[i].reshape(28, 28), cmap="gray")
        plt.axis("off")

        # Reconstructed images
        plt.subplot(2, n, i + 1 + n)
        plt.imshow(decoded_imgs[i].reshape(28, 28), cmap="gray")
        plt.axis("off")
    plt.savefig("autoencoder.png", dpi=300)


visualize_reconstruction(autoencoder, x_test)
