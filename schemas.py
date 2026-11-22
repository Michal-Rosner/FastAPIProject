
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ---------- Users ----------
class UserBase(BaseModel):
    name: str
    email: EmailStr
    username: str


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


# ---------- Projects ----------
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- Tasks ----------
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "todo"
    priority: str = "medium"
    user_id: Optional[int] = None
    project_id: Optional[int] = None


class TaskCreate(TaskBase):
    pass


class TaskResponse(TaskBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True