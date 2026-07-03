from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime
from database.config import get_db
from database.models import Todo, User
from backend.schemas import TodoCreate, TodoResponse
from backend.routers.auth import get_current_user

router = APIRouter(tags=["Todo"])

@router.get("/todos", response_model=list[TodoResponse])
def get_todos(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    todos = db.query(Todo).filter(Todo.user_id == user.id).all()
    return todos

@router.post("/todos", status_code=201, response_model=TodoResponse)
def create_todo(todo_data: TodoCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_todo = Todo(
        id=uuid4(),
        title=todo_data.title,
        description=todo_data.description,
        due_date=todo_data.due_date,
        completed=todo_data.completed,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        user_id=user.id
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@router.get("/todos/{id}", response_model=TodoResponse)
def get_todo(id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == id, Todo.user_id == user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.put("/todos/{id}", response_model=TodoResponse)
def update_todo(id: str, todo_data: TodoCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == id, Todo.user_id == user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.title = todo_data.title
    todo.description = todo_data.description
    todo.due_date = todo_data.due_date
    todo.completed = todo_data.completed
    todo.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(todo)
    return todo

@router.patch("/todos/{id}", response_model=TodoResponse)
def partial_update_todo(id: str, todo_data: TodoCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == id, Todo.user_id == user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    if todo_data.title is not None:
        todo.title = todo_data.title
    if todo_data.description is not None:
        todo.description = todo_data.description
    if todo_data.due_date is not None:
        todo.due_date = todo_data.due_date
    if todo_data.completed is not None:
        todo.completed = todo_data.completed
    todo.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(todo)
    return todo

@router.delete("/todos/{id}")
def delete_todo(id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == id, Todo.user_id == user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"status": "deleted"}