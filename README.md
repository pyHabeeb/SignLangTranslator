# Sign Translation Model C2

A final-year project that translates hand signs into text in real time using:
- **Flask** (web backend)
- **MediaPipe Hands** (hand landmark detection)
- **Scikit-learn RandomForest** (sign classification)
- **OpenCV + JavaScript webcam capture** (live frame input)

## Features

- User registration and login (SQLite)
- Live webcam-based sign prediction
- Text output area for detected words
- Text-to-speech for detected words in browser
- Dataset collection and model training scripts

## Project Structure

```text
Sign Translation Model C2/
├── backend/
│   ├── app.py                    # Flask app + routes + prediction endpoint
│   ├── requirements.txt
│   ├── static/
│   │   ├── script.js             # Webcam capture + /predict calls
│   │   └── style.css
│   ├── templates/
│   │   ├── login.html
│   │   ├── register.html
│   │   └── dashboard.html
│   └── web_model/
│       ├── collect_data.py       # Collect hand landmark dataset
│       ├── train_model.py         # Train classifier and save model.pkl
│       └── data.csv
├── frontend/                      # Optional standalone frontend
├── run_backend.ps1                # One-command backend launcher (Windows)
└── README.md
```

## Requirements

- **Windows 10/11** (recommended)
- **Python 3.11**
- Webcam enabled

> Note: This project currently uses `mediapipe==0.10.9`, which works best with Python 3.11 in this setup.

## Setup (Windows)

From the parent folder that contains both `.venv` and `Sign Translation Model C2`:

```powershell
cd "C:\Users\Ayaz\Downloads\Sign Translation Model C2"
py -3.11 -m venv .venv
& ".\.venv\Scripts\python.exe" -m pip install -r ".\Sign Translation Model C2\backend\requirements.txt"
```

## Run Backend (Recommended)

From the project root where `run_backend.ps1` exists:

```powershell
cd "C:\Users\Ayaz\Downloads\Sign Translation Model C2\Sign Translation Model C2"
powershell -ExecutionPolicy Bypass -File .\run_backend.ps1
```

Then open:

- `http://127.0.0.1:5000`

## Run Backend (Manual)

```powershell
cd "C:\Users\Ayaz\Downloads\Sign Translation Model C2\Sign Translation Model C2\backend"
& "C:\Users\Ayaz\Downloads\Sign Translation Model C2\.venv\Scripts\python.exe" app.py
```

## Model Training Workflow

### 1) Collect data

```powershell
cd "C:\Users\Ayaz\Downloads\Sign Translation Model C2\Sign Translation Model C2\backend\web_model"
& "C:\Users\Ayaz\Downloads\Sign Translation Model C2\.venv\Scripts\python.exe" collect_data.py
```

- Enter a label (example: `Hello`) when prompted.
- Press `q` to stop collection.
- Landmarks + label are appended to `data.csv`.

### 2) Train model

```powershell
cd "C:\Users\Ayaz\Downloads\Sign Translation Model C2\Sign Translation Model C2\backend\web_model"
& "C:\Users\Ayaz\Downloads\Sign Translation Model C2\.venv\Scripts\python.exe" train_model.py
```

This generates `model.pkl` in `backend/web_model/`.

## API

### `POST /predict`

Request JSON:

```json
{
  "image": "data:image/jpeg;base64,..."
}
```

Response JSON:

```json
{
  "text": "Predicted_Label"
}
```

If no hand is detected:

```json
{
  "text": "No Hand Detected"
}
```

## Tech Stack

- Flask
- SQLite3
- OpenCV
- MediaPipe
- NumPy
- Scikit-learn
- Joblib
- HTML/CSS/JavaScript

## Known Notes

- This is an academic/demo project and currently stores passwords in plaintext. For production, use password hashing (`werkzeug.security`) and stronger auth/session settings.
- Flask debug mode is enabled in `backend/app.py` for development.

