from Computer_Vision_Task.dataset import *
import numpy as np
from Computer_Vision_Task.user_io import prepare
import os


def setup_model(no_of_classes):
    data_augmentation = tf.keras.Sequential([
        tf.keras.layers.RandomFlip("horizontal"),
        tf.keras.layers.RandomRotation(0.2),
    ])
    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(180, 180, 3)),
        tf.keras.layers.BatchNormalization(),
        data_augmentation,
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.AveragePooling2D((2, 2)),
        tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Flatten(),
        # tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(no_of_classes, activation='softmax'),
    ])

    model.compile(loss='categorical_crossentropy',
                  optimizer='adam', metrics=['accuracy'])

    return model


def train_model():
    data_dir = os.path.dirname(os.path.abspath(__file__)) + "/Dataset"
    train_ds, val_ds = load_local_dataset(data_dir)
    no_of_classes = len(train_ds.class_names)
    # visualise_data(train_ds)

    (X_train, y_train), (X_test, y_test) = extract_X_and_y(train_ds, no_of_classes), extract_X_and_y(val_ds, no_of_classes)

    model = setup_model(no_of_classes)

    history = model.fit(X_train, y_train, epochs=20, validation_data=(X_test, y_test))
    # 15 epochs => 16%
    # 16 epochs => 17%
    # 18% with avg pooling filter 128, worst 16%, best 20%
    history = history.history
    # for metric, values in history.items():
    #     plt.plot(values, label=metric)
    # plt.legend()
    # plt.grid(True)
    # plt.show()
    print(f"Validate accuracy: {np.mean(history['val_accuracy']):.2f}")

    return model, train_ds


def pipeline(img_filepath):
    model, train_ds = train_model()
    categories = get_class_names(train_ds)
    prediction = model.predict([prepare(img_filepath)])
    prediction = np.ndarray.tolist(prediction)
    idx = 0
    for i in range(1, len(prediction[0])):
        if prediction[0][i] > prediction[0][idx]:
            idx = i
    return categories[idx]


if __name__ == "__main__":
    data_dir = os.path.dirname(os.path.abspath(__file__)) + "/Dataset"
    print(data_dir)
    # # Test input
    # for j in range(3):
    #
    #     prediction = np.ndarray.tolist(prediction)
    #     idx = 0
    #     for i in range(1, len(prediction[0])):
    #         if prediction[0][i] > prediction[0][idx]:
    #             idx = i
    #     print(categories[idx])
