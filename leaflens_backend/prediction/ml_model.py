"""
LeafLens - ML Model Loader (Singleton)
@Maharsh Doshi

Loads the TensorFlow .h5 model once into memory and keeps it
resident for all subsequent requests. This avoids the overhead
of loading a ~2MB model on every single API call.
"""

import logging
import numpy as np
from PIL import Image
from io import BytesIO

logger = logging.getLogger(__name__)

# ─── Singleton Model Instance ────────────────────────────────────────
_model = None

CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]
IMAGE_SIZE = (256, 256)


def get_model():
    """
    Returns the loaded TensorFlow/Keras model.
    Loads it from disk on first call, then caches it.
    """
    global _model
    if _model is None:
        try:
            import tensorflow as tf
            from django.conf import settings

            model_path = settings.ML_MODEL_PATH
            logger.info(f"Loading ML model from: {model_path}")
            _model = tf.keras.models.load_model(model_path, compile=False)
            logger.info("ML model loaded successfully!")
        except Exception as e:
            logger.error(f"Failed to load ML model: {e}")
            raise
    return _model


def preprocess_image(image_bytes: bytes) -> np.ndarray:
    """
    Preprocesses an uploaded image for model inference.
    - Opens the image from bytes
    - Converts to RGB
    - Resizes to 256x256
    - Normalizes pixel values to [0, 1]
    - Adds batch dimension

    NOTE: The saved .h5 model does NOT include a Rescaling layer
    (it was applied externally during training), so we must
    normalize here.
    """
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    image = image.resize(IMAGE_SIZE)
    img_array = np.array(image) / 255.0  # Normalize to [0, 1]
    img_batch = np.expand_dims(img_array, axis=0)  # Add batch dimension
    return img_batch


def predict_disease(image_bytes: bytes) -> dict:
    """
    Runs inference on an image and returns the prediction.

    Returns:
        dict with keys: class, confidence, class_index
    """
    model = get_model()
    img_batch = preprocess_image(image_bytes)

    predictions = model.predict(img_batch)
    predicted_index = int(np.argmax(predictions[0]))
    confidence = float(np.max(predictions[0]))

    return {
        "class": CLASS_NAMES[predicted_index],
        "confidence": round(confidence * 100, 2),
        "class_index": predicted_index,
    }
