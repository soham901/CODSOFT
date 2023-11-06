from src.db import Base, Column, Integer, String, engine, Session
from pydantic import BaseModel
from typing import Union


class ContactModel(BaseModel):
    fullname: str
    email: Union[str, None]
    phone: int


class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fullname = Column(String)
    email = Column(String, default='')
    phone = Column(Integer, unique=True)


def create_contact(db: Session, fullname: str, phone: int, email: str = ''):
    new_contact = Contact(fullname=fullname, phone=phone, email=email)
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact


def read_contact(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()


def update_contact(db: Session, contact_id: int, fullname: str, email: str, phone: int):
    # i want to pass the data if it is not None
    old_contact = read_contact(db, contact_id)
    if fullname is not None:
        old_contact.fullname = fullname
    if email is not None:
        old_contact.email = email
    if phone is not None:
        old_contact.phone = phone
    db.commit()
    db.refresh(old_contact)
    return old_contact


def read_contacts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Contact).offset(skip).limit(limit).all()


def delete_contact(db: Session, contact_id: int):
    contact = read_contact(db, contact_id)
    db.delete(contact)
    db.commit()
    return 1


Base.metadata.create_all(engine)
