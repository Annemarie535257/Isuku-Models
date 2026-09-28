import json
from pathlib import Path

import joblib
from django.conf import settings
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Complaint


MODEL_PATH = settings.BASE_DIR / "model" / "waste_complaint_classifier.joblib"
classifier = joblib.load(MODEL_PATH) if MODEL_PATH.exists() else None


def serialize_complaint(complaint):
    return {
        "id": complaint.id,
        "reported_category": complaint.reported_category,
        "predicted_category": complaint.predicted_category,
        "description": complaint.description,
        "location": complaint.location,
        "attachments": complaint.attachment_names,
        "created_at": complaint.created_at.isoformat(),
    }


@require_http_methods(["GET"])
def health_check(request):
    return JsonResponse({"status": "ok", "model_loaded": classifier is not None})


@csrf_exempt
@require_http_methods(["POST"])
def predict_category(request):
    try:
        payload = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Request body must be valid JSON."}, status=400)

    description = str(payload.get("description", "")).strip()
    if not description:
        return JsonResponse({"error": "A description is required."}, status=400)
    if classifier is None:
        return JsonResponse({"error": "The complaint model is not available."}, status=503)

    prediction = str(classifier.predict([description])[0])
    confidence = None
    if hasattr(classifier, "predict_proba"):
        confidence = round(float(max(classifier.predict_proba([description])[0])) * 100, 1)
    return JsonResponse({"category": prediction, "confidence": confidence})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def complaint_list(request):
    if request.method == "GET":
        complaints = Complaint.objects.all()[:50]
        return JsonResponse({"complaints": [serialize_complaint(item) for item in complaints]})

    description = str(request.POST.get("description", "")).strip()
    location = str(request.POST.get("location", "Kigali, Nyarugenge")).strip()
    reported_category = str(request.POST.get("category", "")).strip()
    if not description or not location:
        return JsonResponse({"error": "Description and location are required."}, status=400)
    if classifier is None:
        return JsonResponse({"error": "The complaint model is not available."}, status=503)

    predicted_category = str(classifier.predict([description])[0])
    attachment_names = []
    for upload in request.FILES.getlist("photos"):
        safe_name = Path(upload.name).name
        saved_path = default_storage.save(f"complaints/{safe_name}", upload)
        attachment_names.append(saved_path)

    complaint = Complaint.objects.create(
        reported_category=reported_category or predicted_category,
        predicted_category=predicted_category,
        description=description,
        location=location,
        attachment_names=attachment_names,
    )
    return JsonResponse({"complaint": serialize_complaint(complaint)}, status=201)


@require_http_methods(["GET"])
def complaint_detail(request, complaint_id):
    try:
        complaint = Complaint.objects.get(id=complaint_id)
    except Complaint.DoesNotExist:
        return JsonResponse({"error": "Complaint not found."}, status=404)
    return JsonResponse({"complaint": serialize_complaint(complaint)})