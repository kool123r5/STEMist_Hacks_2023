import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt

# Load the dataset and obtain class names
train_ds = keras.utils.image_dataset_from_directory(
    directory='/Users/kushalb/Documents/VSCode/nn/trainData',
    labels='inferred',
    label_mode='categorical',
    batch_size=32,
    image_size=(515, 389))
validation_ds = keras.utils.image_dataset_from_directory(
    directory='/Users/kushalb/Documents/VSCode/nn/testData',
    labels='inferred',
    label_mode='categorical',
    batch_size=32,
    image_size=(515, 389))

class_names = train_ds.class_names

# Display some sample images
plt.figure(figsize=(10, 10))
for images, labels in train_ds.take(1):
    for i in range(9):
        ax = plt.subplot(3, 3, i + 1)
        plt.imshow(images[i].numpy().astype("uint8"))
        plt.title(class_names[tf.argmax(labels[i])])
        plt.axis("off")
plt.show()

# Create the CNN model
model = keras.Sequential([
    keras.layers.Input(shape=(515, 389, 3)),  # Input shape should be (image_height, image_width, channels)
    keras.layers.Conv2D(32, (3, 3), activation='relu'),  # Convolutional layer with 32 filters
    keras.layers.MaxPooling2D((2, 2)),  # MaxPooling layer to reduce spatial dimensions
    keras.layers.Conv2D(64, (3, 3), activation='relu'),  # Convolutional layer with 64 filters
    keras.layers.MaxPooling2D((2, 2)),  # MaxPooling layer to reduce spatial dimensions
    keras.layers.Flatten(),  # Flatten the 2D feature maps into a 1D vector
    keras.layers.Dense(100, activation='relu'),  # Fully connected layer with 100 units
    keras.layers.Dense(2, activation="softmax")  # Output layer with 2 units (Gun or No gun)
])

# Compile the model
model.compile(optimizer='adam',
              loss='categorical_crossentropy',  # Use 'categorical_crossentropy' for one-hot encoded labels
              metrics=['accuracy'])

# Fit the model to the data
model.fit(train_ds, epochs=10, validation_data=validation_ds)  # You can adjust the number of epochs as needed
model.save('GunNN.h5')
