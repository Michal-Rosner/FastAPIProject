from security import hash_password
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from models import User, Project, Task
import schemas


# ---------- Users ----------
def get_users(db: Session):
    return db.query(User).all()


def get_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hash_password(user.password)

    # מעבירים את כל השדות יחד עם הסיסמה המוצפנת
    db_user = User(
        name=user.name,
        email=user.email,
        username=user.username,
        password=hashed_password
    )
    db.add(db_user)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        # כדי שנדדע להבא אם זה בגלל username או email תפוס
        raise HTTPException(status_code=400, detail="Username or Email already exists")
    db.refresh(db_user)
    return db_user
def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}


# ---------- Projects ----------
def get_projects(db: Session):
    return db.query(Project).all()


def get_project(db: Session, project_id: int):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


def create_project(db: Session, project: schemas.ProjectCreate):
    db_project = Project(name=project.name, description=project.description)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


# ---------- Tasks ----------
def get_tasks(db: Session):
    return db.query(Task).all()


def get_task(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


def create_task(db: Session, task: schemas.TaskCreate):
    # לוודא שהמשתמש והפרויקט קיימים (אם צוינו)
    if task.user_id is not None:
        get_user(db, task.user_id)
    if task.project_id is not None:
        get_project(db, task.project_id)

    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: int, task_update: schemas.TaskCreate):
    task = get_task(db, task_id)
    data = task_update.model_dump(exclude_unset=True)

    # לוודא ערכים תקינים
    new_status = data.get("status")
    if new_status and new_status not in ["todo", "in_progress", "done"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    new_priority = data.get("priority")
    if new_priority and new_priority not in ["low", "medium", "high"]:
        raise HTTPException(status_code=400, detail="Invalid priority")

    for key, value in data.items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int):
    task = get_task(db, task_id)
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()