from flask import Flask, request, jsonify, send_from_directory, redirect
from flask_cors import CORS
import pickle
import sqlite3
from datetime import datetime
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

app = Flask(__name__, static_folder="../frontend/build", static_url_path="")
CORS(app, resources={r"/predict": {"origins": "*"}, r"/login": {"origins": "*"}, r"/signup": {"origins": "*"}})

# Download NLTK resources
nltk.download('punkt')
nltk.download('punkt_tab')  # Added to fix LookupError
nltk.download('stopwords')

# Define the text processing function before loading the model
def enhanced_text_process(text):
    tokens = word_tokenize(text.lower())
    sentiment_words = ['amazing', 'great', 'best', 'good', 'excellent', 'wonderful', 'bad', 
                       'worst', 'terrible', 'poor', 'love', 'hate', 'awesome', 'horrible']
    filtered_tokens = []
    for word in tokens:
        if (word not in string.punctuation and 
            (word not in stopwords.words('english') or word.lower() in sentiment_words)):
            filtered_tokens.append(word)
    return filtered_tokens

# Load model
try:
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    raise

# Function to predict if a review is fake or real with explanation
def predict_review(review_text, pipeline=model):
    prediction = pipeline.predict([review_text])[0]
    probabilities = pipeline.predict_proba([review_text])[0]
    confidence = probabilities[0] if prediction == "CG" else probabilities[1]
    review_length = len(review_text)
    word_count = len(review_text.split())
    exclamation_count = review_text.count('!')
    is_short = word_count < 5
    is_generic = any(word in review_text.lower() for word in ['amazing', 'great', 'good', 'excellent', 'best'])
    if is_short and is_generic and exclamation_count > 0:
        if confidence < 0.85:
            prediction = "OR"
            confidence = 1 - confidence
    rationale = []
    if is_short:
        rationale.append("Review is very short")
    if is_generic:
        rationale.append("Contains generic positive terms")
    if exclamation_count > 0:
        rationale.append(f"Contains {exclamation_count} exclamation marks")
    return {
        "prediction": prediction,
        "confidence": confidence,
        "review": review_text,
        "characteristics": {
            "length": review_length,
            "word_count": word_count,
            "exclamation_count": exclamation_count,
            "is_short": is_short,
            "is_generic": is_generic
        },
        "rationale": rationale
    }

# Initialize databases
def init_db():
    conn = sqlite3.connect("predictions.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            review TEXT,
            prediction TEXT,
            confidence REAL,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def serve_frontend():
    return redirect("http://localhost:3000")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    review = data.get("review")
    if not review:
        return jsonify({"error": "Review text is required"}), 400

    result = predict_review(review)
    prediction = result["prediction"]
    confidence = result["confidence"]

    conn = sqlite3.connect("predictions.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO predictions (review, prediction, confidence, timestamp) VALUES (?, ?, ?, ?)",
        (review, prediction, confidence, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

    return jsonify(result)

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"success": False, "message": "Username and password are required"}), 400

    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    conn.close()

    if user:
        return jsonify({"success": True, "message": "Login successful"})
    else:
        return jsonify({"success": False, "message": "Invalid credentials"})

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"success": False, "message": "Username and password are required"}), 400

    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password, created_at) VALUES (?, ?, ?)", 
                  (username, password, datetime.now().isoformat()))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"success": False, "message": "Username already exists"}), 400
    conn.close()
    return jsonify({"success": True, "message": "Signup successful"})

if __name__ == "__main__":
    app.run(debug=True)


#curl -X POST -H "Content-Type: application/json" -d "{\"review\":\"This product is amazing!\"}" http://127.0.0.1:5000/predict