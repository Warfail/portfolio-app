from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/profile", tags=["profile"])

@router.get("/", response_model=schemas.ProfileResponse)
def get_profile(db: Session = Depends(get_db)):
    profile = db.query(models.Profile).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.put("/", response_model=schemas.ProfileResponse)
def update_profile(profile_data: schemas.ProfileUpdate, db: Session = Depends(get_db)):
    profile = db.query(models.Profile).first()
    if not profile:
        profile = models.Profile(**profile_data.dict())
        db.add(profile)
    else:
        for key, value in profile_data.dict(exclude_unset=True).items():
            setattr(profile, key, value)
    db.commit()
    db.refresh(profile)
    return profile

@router.get("/public", response_model=schemas.ProfileResponse)
def get_public_profile(db: Session = Depends(get_db)):
    profile = db.query(models.Profile).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile