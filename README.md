# Image-Caption-Generator using Flickr8k Dataset

This project is an AI-powered Image Caption Generator that automatically generates natural language descriptions for images. It combines Computer Vision and Natural Language Processing by using a pre-trained CNN model for feature extraction and an LSTM network for caption generation.

The model is trained on the Flickr8k dataset, which contains 8,000 images with five human-written captions for each image.

---

Features

- Automatic image caption generation
- Image feature extraction using VGG16
- Caption generation using LSTM
- Text preprocessing and tokenization
- BLEU score evaluation
- Save and load trained models
- Easy prediction on new images

---

Dataset

- Dataset: Flickr8k
- Images: 8,000
- Captions: 40,000 (5 captions per image)

Directory structure:

dataset/
│
├── Images/
│   ├── 1000268201_693b08cb0e.jpg
│   ├── 1001773457_577c3a7d70.jpg
│   └── ...
│
└── captions.txt

---

Technologies Used

- Python
- TensorFlow / Keras
- NumPy
- Pandas
- NLTK
- OpenCV
- Pillow
- Scikit-learn
- Matplotlib
- Flask (optional)

---

Installation

Clone the repository:

git clone https://github.com/yourusername/Image-Caption-Generator.git
cd Image-Caption-Generator

Install dependencies:

pip install -r requirements.txt

---

Model Architecture

1. Load and preprocess captions.
2. Extract image features using the pre-trained VGG16 model.
3. Convert captions into numerical sequences using a tokenizer.
4. Train an LSTM-based decoder using image features and caption sequences.
5. Generate captions for unseen images.

---

Training

Run:

python train.py

The trained model, tokenizer, and extracted image features will be saved in the "models/" directory.

---

Prediction

Run:

python predict.py

Example output:

Input Image:
dog.jpg

Generated Caption:
"A dog is running through the grass."

---

Evaluation

The model is evaluated using BLEU scores to measure the similarity between generated captions and reference captions.

---

Future Improvements

- Replace VGG16 with ResNet50 or EfficientNet
- Add Attention Mechanism
- Use Transformer-based image captioning models
- Implement Beam Search decoding
- Deploy with Flask or Streamlit
- Support real-time image uploads

---

Learning Outcomes

- Computer Vision
- Deep Learning
- Image Feature Extraction
- Natural Language Processing
- Sequence Modeling
- CNN-LSTM Architecture
- Model Evaluation
- AI Application Development

---

AI & Data Science Enthusiast
