from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db

router = APIRouter(prefix="/api/skills", tags=["skills"])

@router.get("")
def get_skills(db: Session = Depends(get_db)):
    try:
        skills = db.query(models.Skill).all()
        result = []
        for skill in skills:
            result.append({
                "id": skill.id,
                "category": skill.category,
                "name": skill.name,
                "icon": skill.icon,
                "level": skill.level
            })
        return result
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("")
def create_skill(skill_data: dict, db: Session = Depends(get_db)):
    try:
        skill = models.Skill(**skill_data)
        db.add(skill)
        db.commit()
        db.refresh(skill)
        return {
            "id": skill.id,
            "category": skill.category,
            "name": skill.name,
            "icon": skill.icon,
            "level": skill.level
        }
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{skill_id}")
def delete_skill(skill_id: int, db: Session = Depends(get_db)):
    try:
        skill = db.query(models.Skill).filter(models.Skill.id == skill_id).first()
        if not skill:
            raise HTTPException(status_code=404, detail="Skill not found")
        db.delete(skill)
        db.commit()
        return {"message": "Skill deleted successfully"}
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))