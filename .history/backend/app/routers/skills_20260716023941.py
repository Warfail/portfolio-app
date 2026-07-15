from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/skills", tags=["skills"])

@router.get("/", response_model=List[schemas.SkillResponse])
def get_skills(db: Session = Depends(get_db)):
    return db.query(models.Skill).all()

# Add this to handle requests without trailing slash
@router.get("", response_model=List[schemas.SkillResponse])
def get_skills_no_slash(db: Session = Depends(get_db)):
    return db.query(models.Skill).all()

@router.get("/{skill_id}", response_model=schemas.SkillResponse)
def get_skill(skill_id: int, db: Session = Depends(get_db)):
    skill = db.query(models.Skill).filter(models.Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill

@router.post("/", response_model=schemas.SkillResponse)
def create_skill(skill: schemas.SkillCreate, db: Session = Depends(get_db)):
    db_skill = models.Skill(**skill.dict())
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill

@router.put("/{skill_id}", response_model=schemas.SkillResponse)
def update_skill(skill_id: int, skill_data: schemas.SkillUpdate, db: Session = Depends(get_db)):
    skill = db.query(models.Skill).filter(models.Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    for key, value in skill_data.dict(exclude_unset=True).items():
        setattr(skill, key, value)
    db.commit()
    db.refresh(skill)
    return skill

@router.delete("/{skill_id}")
def delete_skill(skill_id: int, db: Session = Depends(get_db)):
    skill = db.query(models.Skill).filter(models.Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    db.delete(skill)
    db.commit()
    return {"message": "Skill deleted successfully"}