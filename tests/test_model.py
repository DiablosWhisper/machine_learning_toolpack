from networks.network import DeepNetwork
from tensorflow.keras import layers
from tensorflow import keras
import numpy as np

if __name__=="__main__" :
    input_shape=(28, 28, 1)
    num_classes=10

    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

    x_train = x_train.astype("float32") / 255
    x_test = x_test.astype("float32") / 255
    x_train = np.expand_dims(x_train, -1)
    x_test = np.expand_dims(x_test, -1)

    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)

    configuration={
        "structure": [
            dict(cast="Conv2D", kernel_size=(3, 3), activation="relu", input_shape=input_shape, filters=32),
            dict(cast="MaxPooling2D", pool_size=(2, 2)),
            dict(cast="Conv2D", kernel_size=(3, 3), activation="relu", filters=64),
            dict(cast="MaxPooling2D", pool_size=(2, 2)),
            dict(cast="Flatten"),
            dict(cast="Dropout", rate=0.5),
            dict(cast="Dense", units=num_classes, activation="softmax")
        ],
        "compile": {
            "loss": dict(cast="CategoricalCrosentropy"),
            "metrics":[dict(cast="Accuracy")],
            "optimizer": dict(cast="Adam")
        }
    }
    fit=dict(x=x_train, y=y_train, batch_size=128, epochs=15, validation_split=0.1)

    model=DeepNetwork()
    model.compile(configuration)
    model.fit(fit)