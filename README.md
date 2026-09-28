# Isuku Models and Household Complaint App

The saved waste complaint classifier is deployed through Streamlit with a household complaint page and an admin dashboard.

## Streamlit app

Install the project dependencies and start the app from the repository root:

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Streamlit opens the household complaint page. Use the **Admin Dashboard** page in the sidebar to review submitted complaints and model classifications.

The app loads `model/waste_complaint_classifier.joblib` directly, stores complaints in a local SQLite database, and saves uploaded photos in `uploads/`.

The classifier recognizes five categories: missed pickup, delayed pickup, full bin, illegal dumping, and recycling questions. Recycling questions include restaurant leftovers, kitchen scraps, composting, animal feed, donation, and biogas questions.

For Streamlit Community Cloud, set the main file to `streamlit_app.py` and deploy from this repository.

## Legacy Django API

The original Django API files are retained for integrations that still need HTTP endpoints. They are not required by the Streamlit deployment; install the three Django packages separately if you continue using that API.

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install django djangorestframework django-cors-headers
python manage.py migrate
python manage.py runserver
```

The API runs at `http://127.0.0.1:8000`.

- `GET /api/health/` checks API and model availability.
- `POST /api/predict/` accepts JSON with a `description` and returns the predicted category and confidence.
- `POST /api/complaints/` accepts multipart form data (`category`, `description`, `location`, and optional `photos`) and stores the complaint after calling `model/waste_complaint_classifier.joblib`.
- `GET /api/complaints/` lists recent complaints.

