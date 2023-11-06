from fastapi import FastAPI, Form, Request, Depends, Response

from src.utils import Template
from src.db import Session, get_db

from .models import read_todo, read_todos, create_todo, update_todo, delete_todo, complete_todo

app = FastAPI()

template = Template(__package__)


@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    todos = read_todos(db)
    return template.render('home.html', {'request': request, 'todos': todos})


@app.post("/add")
async def add(request: Request, task: str = Form(...), db: Session = Depends(get_db)):
    new_todo = create_todo(db, task)
    return template.render('_item.html', {'request': request, 'todo': new_todo})


@app.delete("/remove/{todo_id}", response_class=Response)
async def remove(todo_id: int, db: Session = Depends(get_db)):
    delete_todo(db, todo_id)


@app.get("/complete/{todo_id}")
async def complete(request: Request, todo_id: int, db: Session = Depends(get_db)):
    complete_todo(db, todo_id)
    todo = read_todo(db, todo_id)
    return template.render('_item.html', {'request': request, 'todo': todo})


@app.get("/edit/{todo_id}")
async def edit(request: Request, todo_id: int, db: Session = Depends(get_db)):
    todo = read_todo(db, todo_id)
    return template.render('_edit.html', {'request': request, 'todo': todo})


@app.post("/edit/{todo_id}")
async def edit(request: Request, todo_id: int, task: str = Form(...), db: Session = Depends(get_db)):
    todo = update_todo(db, todo_id, task)
    return template.render('_item.html', {'request': request, 'todo': todo})
