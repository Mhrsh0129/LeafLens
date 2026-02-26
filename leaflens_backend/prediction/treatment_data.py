"""
LeafLens - Treatment Recommendations Database
@Maharsh Doshi

Contains detailed treatment advice, symptoms, prevention tips,
and contextual weather information for each potato disease.
"""

TREATMENT_DATABASE = {
    "Early Blight": {
        "disease": "Early Blight",
        "scientific_name": "Alternaria solani",
        "symptoms": [
            "Dark brown to black concentric rings (target-like spots) on older, lower leaves",
            "Yellowing of tissue surrounding the lesions",
            "Lesions may also appear on stems and tubers",
            "Premature defoliation in severe cases",
        ],
        "causes": [
            "Fungal pathogen Alternaria solani",
            "Thrives in warm (24-29°C / 75-84°F), humid conditions",
            "Spreads through wind, rain splash, and infected plant debris",
            "Overwinters in soil and plant residues",
        ],
        "treatment": [
            "Apply chlorothalonil-based fungicides (e.g., Bravo, Daconil) at first sign of symptoms",
            "Use mancozeb or copper-based fungicides as preventive sprays",
            "Remove and destroy infected leaves immediately",
            "Apply neem oil as an organic alternative for mild infections",
            "Ensure proper spacing between plants for air circulation",
        ],
        "prevention": [
            "Practice crop rotation — avoid planting potatoes in the same field for 2-3 years",
            "Use certified disease-free seed potatoes",
            "Apply mulch to prevent soil-borne spores from splashing onto leaves",
            "Water at the base of plants (drip irrigation) to keep foliage dry",
            "Remove plant debris after harvest to reduce overwintering spores",
            "Choose resistant varieties when available (e.g., Kennebec, Elba)",
        ],
        "severity": "Moderate",
        "weather_context": {
            "favorable_temp_min": 24,
            "favorable_temp_max": 29,
            "favorable_humidity_min": 70,
            "description": "Early Blight thrives in warm (24-29°C) and humid (>70%) conditions. "
            "Alternating wet and dry weather accelerates spore production.",
        },
    },
    "Late Blight": {
        "disease": "Late Blight",
        "scientific_name": "Phytophthora infestans",
        "symptoms": [
            "Water-soaked, dark green to brown lesions on leaves",
            "White fuzzy mold growth on the underside of leaves in humid conditions",
            "Rapid wilting and browning of entire plants within days",
            "Brown, firm rot on tubers with a granular texture beneath the skin",
            "Foul smell from severely infected plants",
        ],
        "causes": [
            "Oomycete pathogen Phytophthora infestans",
            "Thrives in cool (10-20°C / 50-68°F), wet, and humid conditions",
            "Spreads rapidly through wind-borne spores and rain",
            "Can devastate an entire field within 1-2 weeks if untreated",
            "Historically caused the Irish Potato Famine (1845-1852)",
        ],
        "treatment": [
            "Apply metalaxyl (Ridomil) or cymoxanil-based systemic fungicides IMMEDIATELY",
            "Copper-based fungicides (Bordeaux mixture) as a contact spray",
            "Remove and BURN infected plants — do NOT compost them",
            "Harvest tubers early if infection is spreading uncontrollably",
            "Avoid overhead irrigation during outbreaks",
        ],
        "prevention": [
            "Use certified disease-free, resistant seed potatoes (e.g., Sarpo Mira, Defender)",
            "Apply preventive fungicide sprays before conditions become favorable",
            "Monitor weather forecasts — apply protection before cool, rainy periods",
            "Ensure excellent drainage in fields to prevent waterlogging",
            "Hill up potatoes properly to protect tubers from spore wash-down",
            "Destroy volunteer potato plants and cull piles in spring",
        ],
        "severity": "Severe — Requires IMMEDIATE action",
        "weather_context": {
            "favorable_temp_min": 10,
            "favorable_temp_max": 20,
            "favorable_humidity_min": 80,
            "description": "Late Blight is most dangerous in cool (10-20°C), highly humid (>80%) "
            "conditions with prolonged leaf wetness. Rainy, overcast days are critical risk periods.",
        },
    },
    "Healthy": {
        "disease": "Healthy",
        "scientific_name": "N/A",
        "symptoms": [
            "No visible disease symptoms",
            "Uniform green foliage with no spots or discoloration",
            "Strong stem and leaf structure",
        ],
        "causes": [],
        "treatment": [
            "No treatment required — your plant looks healthy! 🎉",
        ],
        "prevention": [
            "Continue regular monitoring of your crop",
            "Maintain proper irrigation and fertilization schedules",
            "Apply preventive fungicide sprays during favorable disease conditions",
            "Practice crop rotation to maintain soil health",
            "Scout fields regularly, especially during wet weather",
        ],
        "severity": "None",
        "weather_context": {
            "favorable_temp_min": None,
            "favorable_temp_max": None,
            "favorable_humidity_min": None,
            "description": "Your plant is healthy! Keep monitoring weather conditions and "
            "apply preventive measures during cool, humid periods.",
        },
    },
}


def get_treatment(disease_name: str) -> dict:
    """
    Returns the full treatment recommendation for a given disease.

    Args:
        disease_name: One of "Early Blight", "Late Blight", or "Healthy"

    Returns:
        dict with all treatment information
    """
    return TREATMENT_DATABASE.get(disease_name, TREATMENT_DATABASE["Healthy"])


def get_weather_risk_assessment(
    disease_name: str, temperature: float, humidity: float
) -> dict:
    """
    Assess the risk of a disease based on current weather conditions.

    Returns:
        dict with risk_level, risk_message, and weather_favorable
    """
    if disease_name == "Healthy":
        # Check if conditions are favorable for ANY disease
        early_blight_risk = _check_weather_risk("Early Blight", temperature, humidity)
        late_blight_risk = _check_weather_risk("Late Blight", temperature, humidity)

        warnings = []
        if early_blight_risk["weather_favorable"]:
            warnings.append(
                "⚠️ Current weather is favorable for Early Blight. Monitor closely."
            )
        if late_blight_risk["weather_favorable"]:
            warnings.append(
                "⚠️ Current weather is favorable for Late Blight. Consider preventive sprays."
            )

        return {
            "risk_level": "Low" if not warnings else "Moderate",
            "risk_message": " | ".join(warnings)
            if warnings
            else "✅ Weather conditions are not favorable for disease. Keep monitoring!",
            "weather_favorable": bool(warnings),
        }

    return _check_weather_risk(disease_name, temperature, humidity)


def _check_weather_risk(disease_name: str, temperature: float, humidity: float) -> dict:
    """Internal helper to check weather risk for a specific disease."""
    treatment = TREATMENT_DATABASE.get(disease_name)
    if not treatment:
        return {
            "risk_level": "Unknown",
            "risk_message": "Unknown disease.",
            "weather_favorable": False,
        }

    weather_ctx = treatment["weather_context"]
    temp_min = weather_ctx.get("favorable_temp_min")
    temp_max = weather_ctx.get("favorable_temp_max")
    hum_min = weather_ctx.get("favorable_humidity_min")

    if temp_min is None or temp_max is None or hum_min is None:
        return {
            "risk_level": "None",
            "risk_message": "No disease risk.",
            "weather_favorable": False,
        }

    temp_favorable = temp_min <= temperature <= temp_max
    hum_favorable = humidity >= hum_min
    both_favorable = temp_favorable and hum_favorable

    if both_favorable:
        risk_level = "Critical"
        risk_message = (
            f"🚨 CRITICAL: Current temperature ({temperature}°C) and humidity ({humidity}%) "
            f"are HIGHLY favorable for {disease_name}. {weather_ctx['description']} "
            f"Take immediate preventive/treatment action!"
        )
    elif temp_favorable:
        risk_level = "High"
        risk_message = (
            f"⚠️ HIGH RISK: Temperature ({temperature}°C) is in the favorable range for "
            f"{disease_name} ({temp_min}-{temp_max}°C). Monitor humidity closely."
        )
    elif hum_favorable:
        risk_level = "Moderate"
        risk_message = (
            f"⚠️ MODERATE RISK: Humidity ({humidity}%) is favorable for {disease_name} "
            f"(>{hum_min}%). Monitor temperature closely."
        )
    else:
        risk_level = "Low"
        risk_message = (
            f"✅ Current weather (Temp: {temperature}°C, Humidity: {humidity}%) "
            f"is NOT favorable for {disease_name}. Continue monitoring."
        )

    return {
        "risk_level": risk_level,
        "risk_message": risk_message,
        "weather_favorable": both_favorable,
    }
