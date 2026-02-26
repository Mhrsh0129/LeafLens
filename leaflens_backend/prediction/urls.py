"""
LeafLens - Prediction App URL Configuration
@Maharsh Doshi
"""

from django.urls import path
from . import views

app_name = "prediction"

urlpatterns = [
    # Health check
    path("ping/", views.ping, name="ping"),
    # Main prediction endpoint
    path("predict/", views.predict, name="predict"),
    # Treatment recommendations
    path(
        "treatment/<str:disease_name>/", views.treatment_detail, name="treatment-detail"
    ),
    # TFLite model endpoints (for offline mobile inference)
    path("tflite/info/", views.tflite_info, name="tflite-info"),
    path("tflite/download/", views.tflite_download, name="tflite-download"),
]
