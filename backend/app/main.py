from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import os
from pathlib import Path

from .routers import auth, profile, skills, experience, projects, contact, upload
from .database import engine, Base
from .utils.cloudinary import configure_cloudinary

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Portfolio API", version="1.0.0")

# Configure Cloudinary
configure_cloudinary()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers (note: no trailing slash issues now)
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(skills.router)
app.include_router(experience.router)
app.include_router(projects.router)
app.include_router(contact.router)
app.include_router(upload.router)

# Serve static files
static_dir = Path(__file__).parent.parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Serve templates
templates_dir = Path(__file__).parent.parent / "templates"

@app.get("/")
async def serve_index():
    return FileResponse(str(templates_dir / "index.html"))

@app.get("/admin")
async def serve_admin():
    return FileResponse(str(templates_dir / "admin.html"))

@app.get("/login")
async def serve_login():
    return FileResponse(str(templates_dir / "login.html"))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Simple test endpoint
@app.get("/api/test")
async def test_api():
    return {"status": "success", "message": "API is working"}