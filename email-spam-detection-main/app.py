from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, classification_report,
    precision_score, recall_score, f1_score
)
from imblearn.over_sampling import SMOTE
from sklearn.utils.class_weight import compute_class_weight
import numpy as np
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
import logging
import os
import argparse
import webbrowser

# --------------------- Logging Setup ---------------------
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# --------------------- NLTK Setup ------------------------
def download_nltk_data():
    try:
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('omw-1.4', quiet=True)
        logger.info("NLTK data downloaded successfully")
    except Exception as e:
        logger.error(f"Failed to download NLTK data: {str(e)}")
        raise

download_nltk_data()

# --------------------- Flask App Init --------------------
app = Flask(__name__)
CORS(app)

# --------------------- Stopwords -------------------------
custom_stopwords = set(stopwords.words('english')).union({'subject', 'http', 'www', 'com'})

# --------------------- Text Preprocessing ----------------
def preprocess_message(message):
    """
    Clean, tokenize, remove stopwords, and lemmatize text input.
    """
    try:
        message = message.lower().strip()
        message = re.sub(r'http\S+|www\S+|@\S+|\d+', '', message)  # Remove URLs, mentions, numbers
        # Keep punctuation as it contains spam indicators like !, $$, etc.
        words = message.split()
        words = [word for word in words if word not in custom_stopwords]  # Remove stopwords
        lemmatizer = WordNetLemmatizer()
        processed_words = []
        for word in words:
            try:
                lemma = lemmatizer.lemmatize(word)
                processed_words.append(lemma)
            except Exception as e:
                logger.warning(f"Failed to lemmatize word '{word}': {str(e)}")
                processed_words.append(word)
        return ' '.join(processed_words)
    except Exception as e:
        logger.error(f"Error preprocessing message: {str(e)}")
        return message  # fallback to original message

# --------------------- Load Dataset ----------------------
try:
    data = pd.read_csv('data/spam.csv', encoding='latin-1')
    data = data[['v1', 'v2']].rename(columns={'v1': 'label', 'v2': 'text'})

    # fix label mapping based on dataset (ham/spam)
    data['label'] = data['label'].map({'ham': 0, 'spam': 1})
    data = data.dropna(subset=['text', 'label'])
    logger.info(f"Dataset loaded with {len(data)} entries")
except Exception as e:
    logger.error(f"Failed to load dataset: {str(e)}")
    raise

# --------------------- Data Split ------------------------
if len(data) < 2:
    raise ValueError("Dataset too small to split")

X_train, X_test, y_train, y_test = train_test_split(
    data['text'], data['label'], test_size=0.2, random_state=42
)

# --------------------- Preprocess Text -------------------
X_train = [preprocess_message(msg) for msg in X_train]
X_test = [preprocess_message(msg) for msg in X_test]

# --------------------- Vectorization ---------------------
try:
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    logger.info("Vectorization completed successfully")
except Exception as e:
    logger.error(f"Vectorization failed: {str(e)}")
    raise

# --------------------- SMOTE Balancing --------------------
try:
    smote = SMOTE(random_state=42)
    X_train_vec, y_train = smote.fit_resample(X_train_vec, y_train)
    logger.info("SMOTE balancing applied successfully")
except Exception as e:
    logger.error(f"SMOTE failed: {str(e)}")
    raise

# --------------------- Class Weights ----------------------
class_weights = compute_class_weight('balanced', classes=np.array([0, 1]), y=y_train)
class_weights_dict = {0: class_weights[0], 1: class_weights[1]}

# --------------------- Model Training ---------------------
try:
    model = RandomForestClassifier(random_state=42, class_weight=class_weights_dict)
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5]
    }
    grid_search = GridSearchCV(model, param_grid, cv=3, scoring='accuracy', n_jobs=-1)
    grid_search.fit(X_train_vec, y_train)
    model = grid_search.best_estimator_
    logger.info("Model training completed successfully")
except Exception as e:
    logger.error(f"Model training failed: {str(e)}")
    raise

# --------------------- Model Evaluation -------------------
try:
    y_pred = model.predict(X_test_vec)
    logger.info("Model Evaluation Metrics:")
    logger.info(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    logger.info(f"Precision: {precision_score(y_test, y_pred):.4f}")
    logger.info(f"Recall: {recall_score(y_test, y_pred):.4f}")
    logger.info(f"F1 Score: {f1_score(y_test, y_pred):.4f}")
    logger.info("\n" + classification_report(y_test, y_pred))
except Exception as e:
    logger.error(f"Model evaluation failed: {str(e)}")
    raise

# --------------------- API Routes -------------------------
@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict if a given message is spam or safe.
    """
    try:
        user_message = request.json.get('message', '')
        logger.debug(f"Received message: {user_message}")

        if not user_message:
            logger.warning("No message provided in request")
            return jsonify({'error': 'No message provided'}), 400

        user_message_processed = preprocess_message(user_message)
        user_message_vec = vectorizer.transform([user_message_processed])
        prediction = model.predict(user_message_vec)[0]
        result = 'spam' if prediction == 1 else 'safe'

        return jsonify({'message': user_message, 'prediction': result})
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/')
def index():
    return "✅ Email Spam Detection API is running."


@app.route('/web')
def web():
    return render_template('index.html')


def predict_message(message):
    """
    Predict if a single message is spam or safe for CLI usage.
    """
    message_processed = preprocess_message(message)
    message_vec = vectorizer.transform([message_processed])
    prediction = model.predict(message_vec)[0]
    result = 'spam' if prediction == 1 else 'safe'
    return result


# --------------------- Run App ----------------------------
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Email Spam Detection")
    parser.add_argument("--message", type=str, help="Email message to classify.")
    args = parser.parse_args()

    if args.message:
        # If a message is provided via command line, classify it
        prediction = predict_message(args.message)
        print(f"The message is classified as: {prediction}")
    else:
        # Otherwise, start the Flask web server
        port = int(os.environ.get("PORT", 5000))
        url = f"http://127.0.0.1:{port}/web"
        print(f"Starting server... Opening browser at {url}")
        webbrowser.open(url)
        app.run(host="0.0.0.0", port=port, debug=True)

