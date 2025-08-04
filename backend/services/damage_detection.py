# backend/services/damage_detection.py

import tensorflow as tf
import numpy as np
from typing import Dict, Any
import os
from PIL import Image
import logging

# --- Build the correct, robust path to the model ---
try:
    SERVICE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.dirname(os.path.dirname(SERVICE_DIR))
    MODEL_PATH = os.path.join(PROJECT_ROOT, "model", "damage_detection.h5")
    model = tf.keras.models.load_model(MODEL_PATH)
    logging.info("✅ Successfully loaded ML model.")
except Exception as e:
    logging.error(f"Failed to load model from path: {MODEL_PATH}", exc_info=True)
    model = None

def preprocess_image(image_path: str) -> np.ndarray:
    """Prepares an image for model prediction."""
    img = Image.open(image_path)
    img = img.resize((224, 224))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array / 255.0

def analyze_damage(image_path: str) -> Dict[str, Any]:
    """Analyzes an image for damage and returns a structured dictionary."""
    if model is None:
        raise RuntimeError("Model is not loaded; cannot perform analysis.")

    processed_image = preprocess_image(image_path)
    
    prediction = model.predict(processed_image)
    # Use prediction[0][0] for clarity, assuming model output shape is (1, 1)
    damage_detected = bool(prediction[0][0] > 0.5)
    confidence = float(prediction[0][0])
    
    severity = "None"
    
    if damage_detected:
        severity = "Moderate" if confidence > 0.7 else "Minor"
        damage_types = [
            {
                "type": "Scratch", "location": "Front bumper", "severity": severity,
                "coordinates": {"x": 120, "y": 200, "width": 80, "height": 40}
            }
        ]
        cost_estimation = {
            "total_cost": 850.0, "labor_cost": 400.0, "parts_cost": 300.0,
            "paint_cost": 150.0,
            "breakdown": [
                {"item": "Labor", "cost": 400.0, "description": "Repair and painting labor"},
                {"item": "Parts", "cost": 300.0, "description": "Replacement parts"},
                {"item": "Paint", "cost": 150.0, "description": "Paint materials"}
            ]
        }
    else:
        damage_types = []
        cost_estimation = {
            "total_cost": 0.0, "labor_cost": 0.0, "parts_cost": 0.0,
            "paint_cost": 0.0, "breakdown": []
        }
    
    return {
        "damage_detected": damage_detected, "damage_types": damage_types,
        "severity": severity, "cost_estimation": cost_estimation,
        "confidence": confidence
    }