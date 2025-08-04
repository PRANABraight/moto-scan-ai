from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlmodel import Session, select
from datetime import datetime
import os
from pathlib import Path
import tensorflow as tf
import numpy as np
from PIL import Image

from app.db.models import DamageAnalysis
from app.db.database import get_session

router = APIRouter(prefix="/api", tags=["damage-detection"])

# Load the model
model = None
try:
    model = tf.keras.models.load_model("model/damage_detection.h5")
except:
    print("Warning: Could not load model. Running in mock mode.")

def analyze_damage(image_path: str) -> dict:
    """Analyze car damage from an image."""
    try:
        if model is None:
            # Mock response for testing
            return {
                "damage_detected": True,
                "confidence": 0.85,
                "severity": "Medium",
                "damage_types": [{
                    "type": "Scratch",
                    "location": "Front bumper",
                    "severity": "Medium",
                    "coordinates": {"x": 100, "y": 150, "width": 50, "height": 30}
                }],
                "cost_estimation": {
                    "total_cost": 800.0,
                    "labor_cost": 300.0,
                    "parts_cost": 400.0,
                    "paint_cost": 100.0,
                    "breakdown": [{
                        "item": "Labor",
                        "cost": 300.0,
                        "description": "Repair work"
                    }, {
                        "item": "Parts",
                        "cost": 400.0,
                        "description": "Replacement parts"
                    }, {
                        "item": "Paint",
                        "cost": 100.0,
                        "description": "Repainting"
                    }]
                }
            }

        # Load and preprocess the image
        img = Image.open(image_path)
        img = img.resize((224, 224))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Get prediction
        prediction = model.predict(img_array)
        confidence = float(prediction[0][0])
        damage_detected = confidence > 0.5

        # Generate analysis results
        severity = "High" if confidence > 0.8 else "Medium" if confidence > 0.5 else "Low"

        # Cost estimation based on severity
        cost_estimation = {
            "total_cost": 1500.0 if severity == "High" else 800.0 if severity == "Medium" else 300.0,
            "labor_cost": 500.0 if severity == "High" else 300.0 if severity == "Medium" else 100.0,
            "parts_cost": 700.0 if severity == "High" else 400.0 if severity == "Medium" else 150.0,
            "paint_cost": 300.0 if severity == "High" else 100.0 if severity == "Medium" else 50.0,
            "breakdown": [
                {"item": "Labor", "cost": 500.0, "description": "Repair work"},
                {"item": "Parts", "cost": 700.0, "description": "Replacement parts"},
                {"item": "Paint", "cost": 300.0, "description": "Repainting"}
            ] if severity == "High" else []
        }

        damage_types = [
            {
                "type": "Dent" if confidence > 0.7 else "Scratch",
                "location": "Front bumper",
                "severity": severity,
                "coordinates": {"x": 100, "y": 150, "width": 50, "height": 30}
            }
        ] if damage_detected else []

        return {
            "damage_detected": damage_detected,
            "confidence": confidence,
            "severity": severity,
            "damage_types": damage_types,
            "cost_estimation": cost_estimation
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing image: {str(e)}")

@router.post("/analyze", response_model=DamageAnalysis)
async def analyze_image(
    *,
    session: Session = Depends(get_session),
    file: UploadFile = File(...),
    user_id: str
):
    # Create uploads directory if it doesn't exist
    uploads_dir = Path("uploads") / str(user_id)
    uploads_dir.mkdir(parents=True, exist_ok=True)

    # Save the uploaded image
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = uploads_dir / f"{timestamp}_{file.filename}"
    
    with open(image_path, "wb") as image_file:
        content = await file.read()
        image_file.write(content)

    # Analyze the image
    analysis_result = analyze_damage(str(image_path))

    # Create database record
    damage_analysis = DamageAnalysis(
        user_id=user_id,
        image_uri=str(image_path),
        damage_detected=analysis_result["damage_detected"],
        damage_types=analysis_result["damage_types"],
        severity=analysis_result["severity"],
        cost_estimation=analysis_result["cost_estimation"],
        status="Completed",
        confidence=analysis_result["confidence"]
    )

    session.add(damage_analysis)
    session.commit()
    session.refresh(damage_analysis)

    return damage_analysis

@router.get("/{user_id}/history", response_model=list[DamageAnalysis])
def get_user_history(
    *,
    session: Session = Depends(get_session),
    user_id: str
):
    analyses = session.exec(
        select(DamageAnalysis)
        .where(DamageAnalysis.user_id == user_id)
        .order_by(DamageAnalysis.analysis_date.desc())
    ).all()
    return analyses
