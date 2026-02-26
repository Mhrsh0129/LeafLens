"""
LeafLens - Admin Panel Configuration
@Maharsh Doshi
"""

from django.contrib import admin
from .models import ScanHistory


@admin.register(ScanHistory)
class ScanHistoryAdmin(admin.ModelAdmin):
    list_display = [
        "disease_class",
        "confidence",
        "city",
        "temperature",
        "humidity",
        "scanned_at",
    ]
    list_filter = ["disease_class", "scanned_at"]
    search_fields = ["disease_class", "city"]
    readonly_fields = ["scanned_at"]
    ordering = ["-scanned_at"]
