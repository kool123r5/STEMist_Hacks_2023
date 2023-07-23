import tensorflow as tf
import numpy as np
import cv2
from specto import spectrogram

def load_and_preprocess_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.resize(image, (389, 515))
    image = image.astype('float32') / 255.0
    return image

def predict_image(model, image_path):
    image = load_and_preprocess_image(image_path)
    image = np.expand_dims(image, axis=0)
    prediction = model.predict(image)
    return prediction

def tensor(audio_path):
    model_path = 'C:\\Users\\ashwi\\OneDrive\\Documents\\hackathon prep\\hackathon\\GunNN.h5'

    model = tf.keras.models.load_model(model_path)

    spectrogram(audio_path)
    image_path_to_predict = audio_path.replace(".wav", '') + '.png'
    print(image_path_to_predict)



    prediction_result = predict_image(model, image_path_to_predict)
    if(prediction_result[0][1] > 0.6):
        return True
    else:
        return False
    
    # predicted_class_label = np.argmax(prediction_result)
    # print("Predicted class label:", predicted_class_label)
    # if prediction_result.shape[1] == 1:
    #     predicted_class_label = np.argmax(prediction_result)
    #     print("Predicted class label:", predicted_class_label)
    # else:
    #     class_probabilities = prediction_result[0]
    #     num_classes = len(class_probabilities)
    #     for i in range(num_classes):
    #         print(f"Class {i}: Probability = {class_probabilities[i]}")

