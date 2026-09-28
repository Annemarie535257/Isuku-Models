from datetime import datetime, timezone
import sqlite3
from pathlib import Path

import joblib
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model" / "waste_complaint_classifier.joblib"
DATABASE_PATH = BASE_DIR / "complaints.sqlite3"
UPLOADS_DIR = BASE_DIR / "uploads"

CATEGORIES = {
    "missed_pickup": "Missed Pickup",
    "delayed_pickup": "Delayed Pickup",
    "full_bin": "Full Bin",
    "illegal_dumping": "Illegal Dumping",
    "recycling_question": "Recycling Question",
}


def get_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}")
    return joblib.load(MODEL_PATH)


def init_database():
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS complaints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                predicted_category TEXT NOT NULL,
                description TEXT NOT NULL,
                location TEXT NOT NULL,
                photo_names TEXT NOT NULL DEFAULT '',
                status TEXT NOT NULL DEFAULT 'New',
                created_at TEXT NOT NULL
            )
            """
        )


def predict(description):
    model = get_model()
    prediction = str(model.predict([description])[0])
    confidence = None
    if hasattr(model, "predict_proba"):
        confidence = round(float(max(model.predict_proba([description])[0])) * 100, 1)
    return prediction, confidence


def save_complaint(category=None, description="", location="", photo_names=None):
    predicted_category, confidence = predict(description)
    stored_category = category or predicted_category
    created_at = datetime.now(timezone.utc).isoformat()
    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.execute(
            """
            INSERT INTO complaints
                (category, predicted_category, description, location, photo_names, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                stored_category,
                predicted_category,
                description,
                location,
                ",".join(photo_names or []),
                created_at,
            ),
        )
        complaint_id = cursor.lastrowid
    return complaint_id, predicted_category, confidence


def load_complaints():
    init_database()
    with sqlite3.connect(DATABASE_PATH) as connection:
        return pd.read_sql_query(
            "SELECT * FROM complaints ORDER BY datetime(created_at) DESC", connection
        )


def save_uploads(uploaded_files):
    UPLOADS_DIR.mkdir(exist_ok=True)
    saved_names = []
    for uploaded_file in uploaded_files:
        destination = UPLOADS_DIR / Path(uploaded_file.name).name
        destination.write_bytes(uploaded_file.getbuffer())
        saved_names.append(destination.name)
    return saved_names


def display_category(category):
    return CATEGORIES.get(category, category.replace("_", " ").title())


init_database()
