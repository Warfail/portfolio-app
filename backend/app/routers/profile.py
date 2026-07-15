from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from datetime import datetime

router = APIRouter(prefix="/api/profile", tags=["profile"])

@router.get("/public")
def get_public_profile(db: Session = Depends(get_db)):
    try:
        print("🔍 Fetching public profile...")
        profile = db.query(models.Profile).first()
        
        if not profile:
            print("⚠️ No profile found, returning default")
            return {
                "id": 1,
                "name": "Rezky Agung Kurniawan",
                "title": "IT Infrastructure & Desktop Support Specialist",
                "about": "Hi, I'm Rezky Agung Kurniawan, an IT Infrastructure & Desktop Support Specialist passionate about building reliable, secure, and efficient IT environments.",
                "email": "rezkytaewa2@gmail.com",
                "phone": "+62 822-5967-0594",
                "location": "Sleman, Special Region of Yogyakarta, Indonesia",
                "linkedin": "https://www.linkedin.com/in/rezkytaewa",
                "github": "https://github.com/Warfail",
                "profile_image": None
            }
        
        return {
            "id": profile.id,
            "name": profile.name,
            "title": profile.title,
            "about": profile.about,
            "email": profile.email,
            "phone": profile.phone,
            "location": profile.location,
            "linkedin": profile.linkedin,
            "github": profile.github,
            "profile_image": profile.profile_image
        }
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("")
def get_profile(db: Session = Depends(get_db)):
    try:
        profile = db.query(models.Profile).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        return {
            "id": profile.id,
            "name": profile.name,
            "title": profile.title,
            "about": profile.about,
            "email": profile.email,
            "phone": profile.phone,
            "location": profile.location,
            "linkedin": profile.linkedin,
            "github": profile.github,
            "profile_image": profile.profile_image
        }
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))