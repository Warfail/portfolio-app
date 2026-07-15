import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

load_dotenv()

def configure_cloudinary():
    cloudinary.config(
        cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
        api_key=os.getenv('CLOUDINARY_API_KEY'),
        api_secret=os.getenv('CLOUDINARY_API_SECRET')
    )

def upload_image(file, folder='portfolio'):
    configure_cloudinary()
    try:
        result = cloudinary.uploader.upload(
            file.file,
            folder=folder,
            allowed_formats=['jpg', 'jpeg', 'png', 'gif', 'webp']
        )
        return {
            'url': result.get('secure_url'),
            'public_id': result.get('public_id')
        }
    except Exception as e:
        raise Exception(f"Upload failed: {str(e)}")

def delete_image(public_id):
    configure_cloudinary()
    try:
        result = cloudinary.uploader.destroy(public_id)
        return result
    except Exception as e:
        raise Exception(f"Delete failed: {str(e)}")