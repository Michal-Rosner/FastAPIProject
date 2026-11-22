from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
import crud, models, schemas
from database import engine, get_db
from security import verify_password, create_access_token, decode_access_token

app = FastAPI(title="Task Manager API")
bearer_scheme = HTTPBearer(auto_error=False)


# ---------- Auth Dependency ----------
def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None or credentials.scheme.lower() != "bearer":
        raise credentials_exception

    payload = decode_access_token(credentials.credentials)
    if payload is None:
        raise credentials_exception

    subject = payload.get("sub")
    if subject is None:
        raise credentials_exception

    try:
        user_id = int(subject)
    except ValueError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise credentials_exception

    return user


# ---------- Auth ----------
@app.post("/auth/login", response_model=schemas.TokenResponse)
def login(credentials: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, credentials.email)
    if user is None or not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(subject=str(user.id))
    return {"access_token": access_token, "token_type": "bearer"}


# ---------- Users ----------
@app.post("/users", response_model=schemas.UserResponse, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


@app.get("/users/me", response_model=schemas.UserResponse)
def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user


@app.get("/users", response_model=list[schemas.UserResponse])
def get_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.get_users(db)


@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.get_user(db, user_id)


@app.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.delete_user(db, user_id)


# ---------- Projects ----------
@app.post("/projects", response_model=schemas.ProjectResponse, status_code=201)
def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.create_project(db, project)


@app.get("/projects", response_model=list[schemas.ProjectResponse])
def get_projects(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.get_projects(db)


@app.get("/projects/{project_id}", response_model=schemas.ProjectResponse)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.get_project(db, project_id)


# ---------- Tasks ----------
@app.post("/tasks", response_model=schemas.TaskResponse, status_code=201)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.create_task(db, task)


@app.get("/tasks", response_model=list[schemas.TaskResponse])
def get_tasks(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.get_tasks(db)


@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.get_task(db, task_id)


@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(
    task_id: int,
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.update_task(db, task_id, task)


@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.delete_task(db, task_id)