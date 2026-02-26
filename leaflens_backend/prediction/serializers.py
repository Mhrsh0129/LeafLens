"""
LeafLens - DRF Serializers
@Maharsh Doshi
"""

from rest_framework import serializers


class PredictionRequestSerializer(serializers.Serializer):
    """Serializer for the prediction request (image upload + optional GPS)."""

    file = serializers.ImageField(
        required=True, help_text="Image file of the potato plant leaf"
    )
    latitude = serializers.FloatField(
        required=False,
        default=None,
        help_text="GPS latitude for weather-based risk assessment",
    )
    longitude = serializers.FloatField(
        required=False,
        default=None,
        help_text="GPS longitude for weather-based risk assessment",
    )


class WeatherInfoSerializer(serializers.Serializer):
    """Serializer for weather data in the response."""

    temperature = serializers.FloatField()
    feels_like = serializers.FloatField()
    humidity = serializers.IntegerField()
    pressure = serializers.IntegerField()
    description = serializers.CharField()
    wind_speed = serializers.FloatField()
    city = serializers.CharField()
    country = serializers.CharField()
    clouds = serializers.IntegerField()
    rain_1h = serializers.FloatField()
    rain_3h = serializers.FloatField()


class WeatherRiskSerializer(serializers.Serializer):
    """Serializer for weather risk assessment."""

    risk_level = serializers.CharField()
    risk_message = serializers.CharField()
    weather_favorable = serializers.BooleanField()


class TreatmentSerializer(serializers.Serializer):
    """Serializer for treatment recommendations."""

    disease = serializers.CharField()
    scientific_name = serializers.CharField()
    symptoms = serializers.ListField(child=serializers.CharField())
    causes = serializers.ListField(child=serializers.CharField())
    treatment = serializers.ListField(child=serializers.CharField())
    prevention = serializers.ListField(child=serializers.CharField())
    severity = serializers.CharField()


class PredictionResponseSerializer(serializers.Serializer):
    """Full prediction response with disease, treatment, weather, and risk."""

    # Core prediction
    disease_class = serializers.CharField()
    confidence = serializers.FloatField()

    # Treatment recommendations
    treatment_info = TreatmentSerializer()

    # Weather (optional — only if GPS was provided)
    weather = WeatherInfoSerializer(required=False, allow_null=True)
    weather_risk = WeatherRiskSerializer(required=False, allow_null=True)
