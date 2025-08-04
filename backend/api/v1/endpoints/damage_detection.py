from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlmodel import Session, select
from datetime import datetime
import os
from pathlib import Path
from typing import List
import tensorflow as tf
import numpy as np
from PIL import Image

from app.models import DamageAnalysis
from db.database import get_session

router = APIRouter(prefix="/api", tags=["damage-detection"])

# Load the model
model = tf.keras.models.load_model("model/damage_detection.h5")

def analyze_damage(image_path: str) -> dict:
    """Analyze car damage from an image."""
    try:
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

        # Mock cost estimation based on severity
        cost_estimation = {
            "totalCost": 1500 if severity == "High" else 800 if severity == "Medium" else 300,
            "laborCost": 500 if severity == "High" else 300 if severity == "Medium" else 100,
            "partsCost": 700 if severity == "High" else 400 if severity == "Medium" else 150,
            "paintCost": 300 if severity == "High" else 100 if severity == "Medium" else 50,
            "breakdown": [
                {"item": "Labor", "cost": 500, "description": "Repair work"},
                {"item": "Parts", "cost": 700, "description": "Replacement parts"},
                {"item": "Paint", "cost": 300, "description": "Repainting"}
            ] if severity == "High" else []
        }

        # Mock damage types based on severity
        damage_types = [
            {
                "type": "Dent",
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
    user_id: int
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
        image_path=str(image_path),
        damage_detected=analysis_result["damage_detected"],
        confidence=analysis_result["confidence"],
        severity=analysis_result["severity"],
        analysis_data={
            "damage_types": analysis_result["damage_types"],
            "cost_estimation": analysis_result["cost_estimation"]
        }
    )

    session.add(damage_analysis)
    session.commit()
    session.refresh(damage_analysis)

    return damage_analysis

@router.get("/history/{user_id}", response_model=List[DamageAnalysis])
def get_user_history(
    *,
    session: Session = Depends(get_session),
    user_id: int
):
    analyses = session.exec(
        select(DamageAnalysis)
        .where(DamageAnalysis.user_id == user_id)
        .order_by(DamageAnalysis.analysis_date.desc())
    ).all()
    return analyses
