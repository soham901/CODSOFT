from src.db import Base, Column, Integer, String, Boolean, engine, Session


class Todo(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    is_completed = Column(Boolean, default=False)


def create_todo(db: Session, title: str):
    new_todo = Todo(title=title)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


def read_todo(db: Session, todo_id: int):
    return db.query(Todo).filter(Todo.id == todo_id).first()


def update_todo(db: Session, todo_id: int, title: str):
    old_todo = read_todo(db, todo_id)
    old_todo.title = title
    db.commit()
    db.refresh(old_todo)
    return old_todo


def read_todos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Todo).offset(skip).limit(limit).all()


def delete_todo(db: Session, todo_id: int):
    todo = read_todo(db, todo_id)
    db.delete(todo)
    db.commit()
    return 1


def complete_todo(db: Session, item_id: int):
    todo = read_todo(db, item_id)
    todo.is_completed = not todo.is_completed
    db.commit()
    db.refresh(todo)
    return todo


Base.metadata.create_all(engine)
