from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()
db = [] # Database simulasi sementara di memori

class Task(BaseModel):
    id: int
    title: str
    priority: int # Skala 1-3
    completed: bool = False

# --- Business Logic (Fungsi ini yang akan di Unit Test) ---
def is_valid_title(title: str) -> bool:
    # Syarat: Judul minimal 3 karakter dan maksimal 50 karakter
    return 3 <= len(title) <= 50

def is_valid_priority(priority: int) -> bool:
    # Syarat: Prioritas hanya boleh angka 1, 2, atau 3
    return 1 <= priority <= 3

# --- Endpoints API (Fungsi ini yang akan di Integration Test) ---
@app.post("/tasks", status_code=201)
def create_task(task: Task):
    if not is_valid_title(task.title):
        raise HTTPException(status_code=400, detail="Invalid title length")
    if not is_valid_priority(task.priority):
        raise HTTPException(status_code=400, detail="Priority must be 1-3")
    db.append(task.dict())
    return task

@app.get("/tasks")
def get_tasks():
    return db

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    global db
    initial_len = len(db)
    db = [t for t in db if t['id'] != task_id]
    if len(db) == initial_len:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}