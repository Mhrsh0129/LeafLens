"""
LeafLens - Image Validator (Leaf Pre-Check)
@Maharsh Doshi

Validates whether an uploaded image is likely a plant leaf
BEFORE running the ML disease classifier. This prevents
nonsensical predictions on non-leaf images (e.g., selfies, cars).

Technique: Green-channel dominance analysis.
Leaves are predominantly green, so we check if the green channel
is significantly represented in the image's color distribution.
"""

import logging
import numpy as np
from PIL import Image
from io import BytesIO

logger = logging.getLogger(__name__)

# ─── Thresholds (tuned for potato leaf images) ───────────────────────
GREEN_DOMINANCE_THRESHOLD = 0.20  # Min fraction of "green-ish" pixels
MIN_GREEN_RATIO = 1.05  # Green channel must be at least 5% higher than avg of R,B
SATURATION_THRESHOLD = 0.15  # Min average saturation (filters out grayscale images)


def validate_leaf_image(image_bytes: bytes) -> dict:
    """
    Analyzes the image to determine if it likely contains a plant leaf.

    Returns:
        dict with keys:
            - is_leaf: bool — True if the image appears to be a leaf
            - confidence: float — How "leaf-like" the image is (0.0 to 1.0)
            - reason: str — Human-readable explanation
    """
    try:
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
        image = image.resize((128, 128))  # Small size is enough for color analysis
        img_array = np.array(image, dtype=np.float32)

        r_channel = img_array[:, :, 0]
        g_channel = img_array[:, :, 1]
        b_channel = img_array[:, :, 2]

        # ── Check 1: Green channel dominance ──
        # A pixel is "green-ish" if green > red AND green > blue
        green_dominant_pixels = np.logical_and(
            g_channel > r_channel, g_channel > b_channel
        )
        green_fraction = np.mean(green_dominant_pixels)

        # ── Check 2: Green-to-other ratio ──
        avg_green = np.mean(g_channel)
        avg_red = np.mean(r_channel)
        avg_blue = np.mean(b_channel)
        avg_other = (avg_red + avg_blue) / 2.0

        green_ratio = avg_green / max(avg_other, 1.0)

        # ── Check 3: Saturation check (filters grayscale) ──
        max_channel = np.maximum(np.maximum(r_channel, g_channel), b_channel)
        min_channel = np.minimum(np.minimum(r_channel, g_channel), b_channel)
        saturation = np.where(
            max_channel > 0, (max_channel - min_channel) / max_channel, 0
        )
        avg_saturation = np.mean(saturation)

        # ── Compute leaf confidence score ──
        # Weighted combination of the three checks
        score = (
            0.50 * min(green_fraction / GREEN_DOMINANCE_THRESHOLD, 1.0)
            + 0.30 * min(green_ratio / MIN_GREEN_RATIO, 1.0)
            + 0.20 * min(avg_saturation / SATURATION_THRESHOLD, 1.0)
        )
        score = round(float(score), 3)

        is_leaf = (
            green_fraction >= GREEN_DOMINANCE_THRESHOLD
            and green_ratio >= MIN_GREEN_RATIO
            and avg_saturation >= SATURATION_THRESHOLD
        )

        if is_leaf:
            reason = "Image appears to contain a plant leaf."
        else:
            reasons = []
            if green_fraction < GREEN_DOMINANCE_THRESHOLD:
                reasons.append(
                    f"low green content ({green_fraction:.1%} green pixels, need ≥{GREEN_DOMINANCE_THRESHOLD:.0%})"
                )
            if green_ratio < MIN_GREEN_RATIO:
                reasons.append(
                    f"green channel not dominant (ratio {green_ratio:.2f}, need ≥{MIN_GREEN_RATIO})"
                )
            if avg_saturation < SATURATION_THRESHOLD:
                reasons.append(
                    f"low color saturation ({avg_saturation:.2f}, need ≥{SATURATION_THRESHOLD})"
                )
            reason = "Image does not appear to be a plant leaf: " + "; ".join(reasons)

        logger.info(
            f"Leaf validation: is_leaf={is_leaf}, score={score}, "
            f"green_frac={green_fraction:.3f}, green_ratio={green_ratio:.3f}, "
            f"saturation={avg_saturation:.3f}"
        )

        return {
            "is_leaf": is_leaf,
            "confidence": score,
            "reason": reason,
        }

    except Exception as e:
        logger.error(f"Image validation failed: {e}")
        # If validation fails, allow the image through (fail-open)
        return {
            "is_leaf": True,
            "confidence": 0.0,
            "reason": "Validation skipped due to an error.",
        }
