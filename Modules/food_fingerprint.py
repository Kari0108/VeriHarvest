import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Step 1: Load and Preprocess Data
def load_data(directory):
    datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)
    train_data = datagen.flow_from_directory(
        directory,
        target_size=(128, 128),
        batch_size=32,
        class_mode='binary',
        subset='training'
    )
    validation_data = datagen.flow_from_directory(
        directory,
        target_size=(128, 128),
        batch_size=32,
        class_mode='binary',
        subset='validation'
    )
    return train_data, validation_data

# Step 2: Define AI Model
def build_model():
    model = Sequential([
        Conv2D(32, (3,3), activation='relu', input_shape=(128,128,3)),
        MaxPooling2D(2,2),
        Conv2D(64, (3,3), activation='relu'),
        MaxPooling2D(2,2),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# Step 3: Train the Model
def train_model(model, train_data, validation_data, epochs=10):
    model.fit(train_data, validation_data=validation_data, epochs=epochs)
    model.save("food_fingerprint_model.h5")

# Step 4: Predict on New Image
def predict_fingerprint(model_path, image_path):
    model = tf.keras.models.load_model(model_path)
    image = cv2.imread(image_path)
    image = cv2.resize(image, (128, 128))
    image = np.expand_dims(image, axis=0) / 255.0
    prediction = model.predict(image)
    return "Authentic" if prediction > 0.5 else "Fraudulent"

# Running the Pipeline
if __name__ == "__main__":
    train_data, validation_data = load_data("dataset/food_images")
    model = build_model()
    train_model(model, train_data, validation_data)
    result = predict_fingerprint("food_fingerprint_model.h5", "dataset/test_image.jpg")
    print(f"Food Authentication Result: {result}")
