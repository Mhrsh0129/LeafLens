"""
LeafLens - Weather Service (OpenWeatherMap Integration)
@Maharsh Doshi

Fetches real-time weather data for a given GPS location
to provide contextual disease risk assessment.
"""

import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

OPENWEATHERMAP_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather_data(latitude: float, longitude: float) -> dict | None:
    """
    Fetches current weather data from OpenWeatherMap for given coordinates.

    Args:
        latitude: GPS latitude
        longitude: GPS longitude

    Returns:
        dict with weather data or None if the API call fails
    """
    api_key = settings.OPENWEATHERMAP_API_KEY

    if not api_key:
        logger.warning(
            "OpenWeatherMap API key not configured. "
            "Set OPENWEATHERMAP_API_KEY in your .env file. "
            "Get a free key at: https://openweathermap.org/api"
        )
        return None

    try:
        params = {
            "lat": latitude,
            "lon": longitude,
            "appid": api_key,
            "units": "metric",  # Celsius
        }

        response = requests.get(OPENWEATHERMAP_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        weather_info = {
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "description": data["weather"][0]["description"].title(),
            "wind_speed": data["wind"]["speed"],
            "city": data.get("name", "Unknown"),
            "country": data.get("sys", {}).get("country", ""),
            "clouds": data.get("clouds", {}).get("all", 0),
        }

        # Check for rain data
        if "rain" in data:
            weather_info["rain_1h"] = data["rain"].get("1h", 0)
            weather_info["rain_3h"] = data["rain"].get("3h", 0)
        else:
            weather_info["rain_1h"] = 0
            weather_info["rain_3h"] = 0

        logger.info(
            f"Weather fetched for ({latitude}, {longitude}): "
            f"{weather_info['temperature']}°C, {weather_info['humidity']}% humidity"
        )

        return weather_info

    except requests.exceptions.Timeout:
        logger.error("OpenWeatherMap API request timed out")
        return None
    except requests.exceptions.HTTPError as e:
        logger.error(f"OpenWeatherMap API error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch weather data: {e}")
        return None
    except (KeyError, IndexError) as e:
        logger.error(f"Unexpected weather API response format: {e}")
        return None
