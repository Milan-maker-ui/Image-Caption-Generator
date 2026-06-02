import pickle
import numpy as np

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model

# Load Saved Model & Files

model_caption = load_model(r"C:\Users\arote\OneDrive\Desktop\Image caption Generator\models\image_caption_model.keras", compile=False)

with open(r"models\tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

with open(r"models\max_length.pkl", "rb") as f:
    max_length = pickle.load(f)

# VGG16 Feature Extractor

base_model = VGG16()
feature_model = Model( inputs=base_model.inputs, outputs=base_model.layers[-2].output)

# Convert Index To Word

def idx_to_word(integer, tokenizer):
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None

# Extract Features

def extract_features(filename):
    image = load_img(filename, target_size=(224, 224))
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = preprocess_input(image)
    feature = feature_model.predict(image, verbose=0)
    return feature

# Generate Caption

def generate_caption(image_path):
    photo = extract_features(image_path)
    print("Feature Shape:", photo.shape)
    in_text = "startseq"
    for i in range(max_length):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], maxlen=max_length)
        yhat = model_caption.predict([photo, sequence], verbose=0)
        yhat = np.argmax(yhat)
        word = idx_to_word(yhat, tokenizer)
        if word is None:
            break

        in_text += " " + word

        if word == "endseq":
            break

    caption = in_text.replace("startseq", "" )
    caption = caption.replace( "endseq", "" )
    return caption.strip()

# Test

if __name__ == "__main__":

    image_path = r"dataset/images/1000268201_693b08cb0e.jpg"
    caption = generate_caption(image_path)

    print("\nGenerated Caption:")
    print(caption)