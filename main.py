from fastapi import FastAPI
from database import engine, SessionLocal
from models import Task, Base
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/tasks")
def get_tasks():
    db = SessionLocal()
    return db.query(Task).all()

@app.post("/tasks")
def create_task(task: dict):
    db = SessionLocal()
    new_task = Task(title=task["title"])
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.put("/tasks/{task_id}")
def complete_task(task_id: int):
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()
    task.completed = True
    db.commit()
    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()
    db.delete(task)
    db.commit()
    return {"message": "Deleted"}
@app.get("/")
def root():
    return {"message": "Wellcome to FastApi Server"}