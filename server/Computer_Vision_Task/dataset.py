import tensorflow as tf
import matplotlib.pyplot as plt


def load_local_dataset(data_dir: str):
    # Load dataset from directory
    batch_size = 32
    img_height = 180
    img_width = 180

    train_ds = tf.keras.utils.image_dataset_from_directory(
              data_dir,
              validation_split=0.2,
              subset="training",
              seed=123,
              image_size=(img_height, img_width),
              batch_size=batch_size
    )

    val_ds = tf.keras.utils.image_dataset_from_directory(
              data_dir,
              validation_split=0.2,
              subset="validation",
              seed=123,
              image_size=(img_height, img_width),
              batch_size=batch_size
    )

    return train_ds, val_ds


def get_class_names(train_ds):
    class_names = train_ds.class_names
    print(class_names)

    return class_names


def visualise_data(train_ds):
    class_names = get_class_names(train_ds)

    plt.figure(figsize=(10, 10))
    for images, labels in train_ds.take(1):
      for i in range(9):
        ax = plt.subplot(3, 3, i + 1)
        plt.imshow(images[i].numpy().astype("uint8"))
        plt.title(class_names[labels[i]])
        plt.axis("off")

    plt.show()


def extract_X_and_y(ds, no_of_classes):
    X, y = [], []

    for images, labels in ds:
        X.append(images.numpy())
        y.append(labels.numpy())

    X = tf.concat(X, axis=0)
    y = tf.concat(y, axis=0)

    y = tf.keras.utils.to_categorical(y, num_classes=no_of_classes)
    return X, y


