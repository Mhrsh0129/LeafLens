"""
LeafLens - Database Models
@Maharsh Doshi

Stores scan history so users can track disease progression over time.
"""

from django.db import models


class ScanHistory(models.Model):
    """Records each disease scan performed through the API."""

    DISEASE_CHOICES = [
        ("Early Blight", "Early Blight"),
        ("Late Blight", "Late Blight"),
        ("Healthy", "Healthy"),
    ]

    # Prediction results
    disease_class = models.CharField(max_length=50, choices=DISEASE_CHOICES)
    confidence = models.FloatField(help_text="Confidence percentage (0-100)")

    # Location (optional)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)

    # Weather at the time of scan (optional)
    temperature = models.FloatField(
        null=True, blank=True, help_text="Temperature in °C"
    )
    humidity = models.FloatField(null=True, blank=True, help_text="Humidity percentage")
    weather_description = models.CharField(max_length=100, null=True, blank=True)

    # Metadata
    scanned_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="scans/%Y/%m/%d/", null=True, blank=True)

    class Meta:
        ordering = ["-scanned_at"]
        verbose_name = "Scan History"
        verbose_name_plural = "Scan Histories"

    def __str__(self):
        return f"{self.disease_class} ({self.confidence}%) - {self.scanned_at.strftime('%Y-%m-%d %H:%M')}"
