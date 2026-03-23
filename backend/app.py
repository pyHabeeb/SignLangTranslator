from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
import cv2
import mediapipe as mp
import joblib
import numpy as np
import base64

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Load trained model
model = joblib.load("web_model/model.pkl")

# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# ---------------- DATABASE ---------------- #

def init_db():
    conn = sqlite3.connect("database.db")
    conn.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  password TEXT)''')
    conn.close()

init_db()

# ---------------- ROUTES ---------------- #

@app.route('/')
def home():
    if "user" in session:
        return redirect("/dashboard")
    return redirect("/login")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")


@app.route('/login', methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            session["user"] = username
            return redirect("/dashboard")

    return render_template("login.html")


@app.route('/dashboard')
def dashboard():

    if "user" not in session:
        return redirect("/login")

    return render_template("dashboard.html")


@app.route('/logout')
def logout():

    session.pop("user", None)
    return redirect("/login")

# ---------------- PREDICTION ---------------- #

@app.route('/predict', methods=['POST'])
def predict():

    data = request.json['image']

    # Decode image
    image_data = base64.b64decode(data.split(',')[1])
    np_img = np.frombuffer(image_data, np.uint8)
    frame = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:

        for hand_landmarks in result.multi_hand_landmarks:

            row = []

            for lm in hand_landmarks.landmark:
                row.extend([lm.x, lm.y, lm.z])

            prediction = model.predict([row])

            return jsonify({"text": prediction[0]})

    return jsonify({"text": "No Hand Detected"})

# ---------------- RUN SERVER ---------------- #

if __name__ == '__main__':
    app.run(debug=True)