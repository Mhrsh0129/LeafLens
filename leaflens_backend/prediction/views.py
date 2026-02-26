"""
LeafLens - API Views
@Maharsh Doshi

Endpoints:
    POST /api/predict/           — Upload image, get disease prediction + treatment + weather risk
    GET  /api/ping/              — Health check
    GET  /api/tflite/download/   — Download TFLite model for offline inference
    GET  /api/treatment/<disease>/ — Get treatment info for a specific disease
"""

import os
import logging

from django.conf import settings
from django.http import FileResponse, Http404
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from .ml_model import predict_disease
from .treatment_data import get_treatment, get_weather_risk_assessment
from .weather_service import get_weather_data
from .image_validator import validate_leaf_image

logger = logging.getLogger(__name__)


# ─── Health Check ────────────────────────────────────────────────────


@api_view(["GET"])
def ping(request):
    """Health check endpoint."""
    return Response(
        {
            "status": "alive",
            "service": "LeafLens API",
            "version": "2.0.0",
            "author": "@Maharsh Doshi",
        }
    )


# ─── Main Prediction Endpoint ───────────────────────────────────────


@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def predict(request):
    """
    Upload a potato leaf image and get:
    1. Disease prediction (class + confidence)
    2. Treatment recommendations (symptoms, treatment, prevention)
    3. Weather-based risk assessment (if GPS coordinates are provided)

    Request:
        POST /api/predict/
        Content-Type: multipart/form-data
        Body:
            - file: Image file (required)
            - latitude: float (optional)
            - longitude: float (optional)

    Response:
        {
            "disease_class": "Late Blight",
            "confidence": 98.5,
            "treatment_info": { ... },
            "weather": { ... } | null,
            "weather_risk": { ... } | null
        }
    """

    # ── Validate image ──
    if "file" not in request.FILES:
        return Response(
            {"error": "No image file provided. Send a 'file' field with your image."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    image_file = request.FILES["file"]

    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/jpg", "image/webp"]
    if image_file.content_type not in allowed_types:
        return Response(
            {
                "error": f"Invalid file type: {image_file.content_type}. Allowed: {', '.join(allowed_types)}"
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        # ── Run ML prediction ──
        image_bytes = image_file.read()

        # ── Validate: is this actually a leaf? ──
        validation = validate_leaf_image(image_bytes)
        if not validation["is_leaf"]:
            return Response(
                {
                    "disease_class": "Not a Leaf",
                    "confidence": 0,
                    "is_leaf": False,
                    "validation_message": validation["reason"],
                    "treatment_info": None,
                    "weather": None,
                    "weather_risk": None,
                },
                status=status.HTTP_200_OK,
            )

        prediction = predict_disease(image_bytes)

        disease_class = prediction["class"]
        confidence = prediction["confidence"]

        # ── Get treatment recommendations ──
        treatment_info = get_treatment(disease_class)

        # ── Weather & Risk Assessment (optional) ──
        weather_data = None
        weather_risk = None

        latitude = request.data.get("latitude") or request.query_params.get("latitude")
        longitude = request.data.get("longitude") or request.query_params.get(
            "longitude"
        )

        if latitude is not None and longitude is not None:
            try:
                lat = float(latitude)
                lon = float(longitude)
                weather_data = get_weather_data(lat, lon)

                if weather_data:
                    weather_risk = get_weather_risk_assessment(
                        disease_class,
                        weather_data["temperature"],
                        weather_data["humidity"],
                    )
            except (ValueError, TypeError) as e:
                logger.warning(
                    f"Invalid GPS coordinates: lat={latitude}, lon={longitude}. Error: {e}"
                )

        # ── Build response ──
        response_data = {
            "disease_class": disease_class,
            "confidence": confidence,
            "treatment_info": {
                "disease": treatment_info["disease"],
                "scientific_name": treatment_info["scientific_name"],
                "symptoms": treatment_info["symptoms"],
                "causes": treatment_info["causes"],
                "treatment": treatment_info["treatment"],
                "prevention": treatment_info["prevention"],
                "severity": treatment_info["severity"],
            },
            "weather": weather_data,
            "weather_risk": weather_risk,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Prediction failed: {e}", exc_info=True)
        return Response(
            {"error": f"Prediction failed: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# ─── Treatment Info Endpoint ─────────────────────────────────────────


@api_view(["GET"])
def treatment_detail(request, disease_name):
    """
    Get treatment details for a specific disease.

    GET /api/treatment/Early Blight/
    GET /api/treatment/Late Blight/
    GET /api/treatment/Healthy/
    """
    valid_diseases = ["Early Blight", "Late Blight", "Healthy"]
    if disease_name not in valid_diseases:
        return Response(
            {
                "error": f"Unknown disease: '{disease_name}'. Valid options: {valid_diseases}"
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    treatment = get_treatment(disease_name)
    return Response(treatment, status=status.HTTP_200_OK)


# ─── TFLite Model Download Endpoint ─────────────────────────────────


@api_view(["GET"])
def tflite_download(request):
    """
    Download the TFLite model for offline inference on mobile devices.

    GET /api/tflite/download/
    GET /api/tflite/download/?version=1  (default)
    GET /api/tflite/download/?version=2  (quantized)

    The mobile app can download this model and run inference locally
    without needing an internet connection.
    """
    version = request.query_params.get("version", "2")
    model_filename = f"{version}.tflite"
    model_path = os.path.join(settings.TFLITE_MODELS_DIR, model_filename)

    if not os.path.exists(model_path):
        available = []
        tflite_dir = settings.TFLITE_MODELS_DIR
        if os.path.exists(tflite_dir):
            available = [f for f in os.listdir(tflite_dir) if f.endswith(".tflite")]

        return Response(
            {
                "error": f"TFLite model version '{version}' not found.",
                "available_versions": [f.replace(".tflite", "") for f in available],
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    # Get file size for the response header
    file_size = os.path.getsize(model_path)

    response = FileResponse(
        open(model_path, "rb"),
        content_type="application/octet-stream",
    )
    response["Content-Disposition"] = (
        f'attachment; filename="leaflens_v{version}.tflite"'
    )
    response["Content-Length"] = file_size
    response["X-Model-Version"] = version
    response["X-Model-Classes"] = "Early Blight,Late Blight,Healthy"
    response["X-Model-Input-Size"] = "256x256"

    logger.info(f"TFLite model v{version} downloaded ({file_size} bytes)")
    return response


# ─── TFLite Model Info Endpoint ──────────────────────────────────────


@api_view(["GET"])
def tflite_info(request):
    """
    Returns metadata about available TFLite models for the mobile app
    to decide whether to download/update its local model.

    GET /api/tflite/info/
    """
    tflite_dir = settings.TFLITE_MODELS_DIR
    models = []

    if os.path.exists(tflite_dir):
        for filename in sorted(os.listdir(tflite_dir)):
            if filename.endswith(".tflite"):
                filepath = os.path.join(tflite_dir, filename)
                version = filename.replace(".tflite", "")
                models.append(
                    {
                        "version": version,
                        "filename": filename,
                        "size_bytes": os.path.getsize(filepath),
                        "size_kb": round(os.path.getsize(filepath) / 1024, 1),
                        "download_url": f"/api/tflite/download/?version={version}",
                    }
                )

    return Response(
        {
            "available_models": models,
            "recommended_version": "2",
            "input_size": "256x256",
            "class_names": ["Early Blight", "Late Blight", "Healthy"],
            "description": "Download a TFLite model for offline potato disease classification on mobile devices.",
        }
    )
