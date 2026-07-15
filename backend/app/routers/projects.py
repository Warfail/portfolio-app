from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db

router = APIRouter(prefix="/api/projects", tags=["projects"])

@router.get("")
def get_projects(db: Session = Depends(get_db)):
    try:
        projects = db.query(models.Project).order_by(models.Project.created_at.desc()).all()
        result = []
        for project in projects:
            result.append({
                "id": project.id,
                "title": project.title,
                "description": project.description,
                "technologies": project.technologies,
                "image_url": project.image_url,
                "project_url": project.project_url,
                "github_url": project.github_url,
                "featured": project.featured
            })
        return result
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))