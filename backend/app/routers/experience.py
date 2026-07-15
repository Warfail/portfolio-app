from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/experience", tags=["experience"])

@router.get("")
def get_experiences(db: Session = Depends(get_db)):
    try:
        experiences = db.query(models.Experience).order_by(models.Experience.start_date.desc()).all()
        result = []
        for exp in experiences:
            result.append({
                "id": exp.id,
                "company": exp.company,
                "position": exp.position,
                "location": exp.location,
                "start_date": exp.start_date.isoformat() if exp.start_date else None,
                "end_date": exp.end_date.isoformat() if exp.end_date else None,
                "is_current": exp.is_current,
                "description": exp.description,
                "achievements": exp.achievements,
                "image_url": exp.image_url  # Add this line
            })
        return result
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{exp_id}")
def get_experience(exp_id: int, db: Session = Depends(get_db)):
    try:
        exp = db.query(models.Experience).filter(models.Experience.id == exp_id).first()
        if not exp:
            raise HTTPException(status_code=404, detail="Experience not found")
        return {
            "id": exp.id,
            "company": exp.company,
            "position": exp.position,
            "location": exp.location,
            "start_date": exp.start_date.isoformat() if exp.start_date else None,
            "end_date": exp.end_date.isoformat() if exp.end_date else None,
            "is_current": exp.is_current,
            "description": exp.description,
            "achievements": exp.achievements,
            "image_url": exp.image_url  # Add this line
        }
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("")
def create_experience(exp_data: dict, db: Session = Depends(get_db)):
    try:
        exp = models.Experience(**exp_data)
        db.add(exp)
        db.commit()
        db.refresh(exp)
        return {
            "id": exp.id,
            "company": exp.company,
            "position": exp.position,
            "location": exp.location,
            "start_date": exp.start_date.isoformat() if exp.start_date else None,
            "end_date": exp.end_date.isoformat() if exp.end_date else None,
            "is_current": exp.is_current,
            "description": exp.description,
            "achievements": exp.achievements,
            "image_url": exp.image_url  # Add this line
        }
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{exp_id}")
def update_experience(exp_id: int, exp_data: dict, db: Session = Depends(get_db)):
    try:
        exp = db.query(models.Experience).filter(models.Experience.id == exp_id).first()
        if not exp:
            raise HTTPException(status_code=404, detail="Experience not found")
        
        for key, value in exp_data.items():
            setattr(exp, key, value)
        
        db.commit()
        db.refresh(exp)
        return {
            "id": exp.id,
            "company": exp.company,
            "position": exp.position,
            "location": exp.location,
            "start_date": exp.start_date.isoformat() if exp.start_date else None,
            "end_date": exp.end_date.isoformat() if exp.end_date else None,
            "is_current": exp.is_current,
            "description": exp.description,
            "achievements": exp.achievements,
            "image_url": exp.image_url  # Add this line
        }
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{exp_id}")
def delete_experience(exp_id: int, db: Session = Depends(get_db)):
    try:
        exp = db.query(models.Experience).filter(models.Experience.id == exp_id).first()
        if not exp:
            raise HTTPException(status_code=404, detail="Experience not found")
        db.delete(exp)
        db.commit()
        return {"message": "Experience deleted successfully"}
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))