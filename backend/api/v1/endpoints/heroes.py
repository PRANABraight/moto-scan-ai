from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlmodel import Session, select
from typing import List
import os
from datetime import datetime

from app.db.database import get_session
from app.db.models import DamageAnalysis, User
from app.services.damage_detection import analyze_damage

router = APIRouter(prefix="/api", tags=["damage-detection"])

@router.post("/analyze", response_model=DamageAnalysis)
async def analyze_image(
    *,
    session: Session = Depends(get_session),
    file: UploadFile = File(...),
    user_id: str
):
    # Save the uploaded image
    image_path = f"uploads/{user_id}/{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
    os.makedirs(os.path.dirname(image_path), exist_ok=True)
    
    with open(image_path, "wb") as image_file:
        content = await file.read()
        image_file.write(content)
    
    # Analyze the image
    analysis_result = analyze_damage(image_path)
    
    # Create database record
    damage_analysis = DamageAnalysis(
        user_id=user_id,
        image_uri=image_path,
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

@router.get("/history/{user_id}", response_model=List[DamageAnalysis])
def get_user_history(*, session: Session = Depends(get_session), user_id: str):
    analyses = session.exec(
        select(DamageAnalysis)
        .where(DamageAnalysis.user_id == user_id)
        .order_by(DamageAnalysis.analysis_date.desc())
    ).all()
    return analyses

@router.get("/analysis/{analysis_id}", response_model=DamageAnalysis)
def get_analysis(*, session: Session = Depends(get_session), analysis_id: int):
    analysis = session.get(DamageAnalysis, analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis
