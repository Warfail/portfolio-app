from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Any

class ProfileBase(BaseModel):
    name: str
    title: str
    about: str
    email: str
    phone: str
    location: str
    linkedin: Optional[str] = None
    github: Optional[str] = None
    profile_image: Optional[str] = None

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    title: Optional[str] = None
    about: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    profile_image: Optional[str] = None

class ProfileResponse(ProfileBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class SkillBase(BaseModel):
    category: str
    name: str
    icon: Optional[str] = None
    level: Optional[int] = None

class SkillCreate(SkillBase):
    pass

class SkillUpdate(BaseModel):
    category: Optional[str] = None
    name: Optional[str] = None
    icon: Optional[str] = None
    level: Optional[int] = None

class SkillResponse(SkillBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ExperienceBase(BaseModel):
    company: str
    position: str
    location: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    is_current: bool = False
    description: Optional[str] = None
    achievements: Optional[List[str]] = None

class ExperienceCreate(ExperienceBase):
    pass

class ExperienceUpdate(BaseModel):
    company: Optional[str] = None
    position: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_current: Optional[bool] = None
    description: Optional[str] = None
    achievements: Optional[List[str]] = None

class ExperienceResponse(ExperienceBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ProjectBase(BaseModel):
    title: str
    description: str
    technologies: Optional[List[str]] = None
    image_url: Optional[str] = None
    project_url: Optional[str] = None
    github_url: Optional[str] = None
    featured: bool = False

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    technologies: Optional[List[str]] = None
    image_url: Optional[str] = None
    project_url: Optional[str] = None
    github_url: Optional[str] = None
    featured: Optional[bool] = None

class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ContactBase(BaseModel):
    name: str
    email: str
    subject: str
    message: str

class ContactCreate(ContactBase):
    pass

class ContactResponse(ContactBase):
    id: int
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True

class AdminLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str