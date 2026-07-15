from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models
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
                "achievements": exp.achievements
            })
        return result
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))