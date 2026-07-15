from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/experience", tags=["experience"])

@router.get("/", response_model=List[schemas.ExperienceResponse])
def get_experiences(db: Session = Depends(get_db)):
    return db.query(models.Experience).order_by(models.Experience.start_date.desc()).all()

@router.get("", response_model=List[schemas.ExperienceResponse])
def get_experiences_no_slash(db: Session = Depends(get_db)):
    return db.query(models.Experience).order_by(models.Experience.start_date.desc()).all()

@router.get("/{exp_id}", response_model=schemas.ExperienceResponse)
def get_experience(exp_id: int, db: Session = Depends(get_db)):
    exp = db.query(models.Experience).filter(models.Experience.id == exp_id).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Experience not found")
    return exp

@router.post("/", response_model=schemas.ExperienceResponse)
def create_experience(exp: schemas.ExperienceCreate, db: Session = Depends(get_db)):
    db_exp = models.Experience(**exp.dict())
    db.add(db_exp)
    db.commit()
    db.refresh(db_exp)
    return db_exp

@router.put("/{exp_id}", response_model=schemas.ExperienceResponse)
def update_experience(exp_id: int, exp_data: schemas.ExperienceUpdate, db: Session = Depends(get_db)):
    exp = db.query(models.Experience).filter(models.Experience.id == exp_id).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Experience not found")
    for key, value in exp_data.dict(exclude_unset=True).items():
        setattr(exp, key, value)
    db.commit()
    db.refresh(exp)
    return exp

@router.delete("/{exp_id}")
def delete_experience(exp_id: int, db: Session = Depends(get_db)):
    exp = db.query(models.Experience).filter(models.Experience.id == exp_id).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Experience not found")
    db.delete(exp)
    db.commit()
    return {"message": "Experience deleted successfully"}