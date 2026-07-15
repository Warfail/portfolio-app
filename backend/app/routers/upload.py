from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from ..utils.cloudinary import upload_image, delete_image
from typing import Dict, Any

router = APIRouter(prefix="/api/upload", tags=["upload"])

@router.post("/image")
async def upload_image_endpoint(file: UploadFile = File(...)) -> Dict[str, Any]:
    try:
        allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="File type not allowed")
        
        result = upload_image(file)
        return {
            "url": result['url'],
            "public_id": result['public_id']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/image/{public_id}")
def delete_image_endpoint(public_id: str):
    try:
        result = delete_image(public_id)
        return {"message": "Image deleted successfully", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))