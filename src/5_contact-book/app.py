import re

from fastapi import FastAPI, Form, Depends, Response
from fastapi.responses import HTMLResponse
from src.utils import Template, Request

from src.db import Session, get_db
from .models import read_contact, read_contacts, create_contact, update_contact, delete_contact

app = FastAPI()

template = Template(__package__)


def is_valid_phone(phone: int):
    phone_number_regex = re.compile(r'^[0-9]{10}$')
    match = phone_number_regex.match(str(phone))
    return match


@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    contacts = sorted(read_contacts(db), key=lambda x: x.id, reverse=True)
    context = {"request": request, "contacts": contacts}
    return template.render("home.html", context)


@app.get("/{contact_id}")
async def details(request: Request, contact_id: int, db: Session = Depends(get_db)):
    contact = read_contact(db, contact_id)
    context = {'request': request, 'contact': contact}
    return template.render('_item.html', context)


@app.post("/add")
async def add(request: Request, fullname: str = Form(...), phone: int = Form(...), email: str = Form(default=''),
              db: Session = Depends(get_db)):
    print(fullname, phone, email)

    try:
        if is_valid_phone(phone):
            contact = create_contact(db=db, fullname=fullname, phone=phone, email=email)
            context = {'request': request, 'contact': contact}
            return template.render('_item.html', context)
        else:
            return HTMLResponse('<script>alert("Phone number is not valid");</script>')

    except Exception as e:
        return HTMLResponse(f'''<script>alert("Error: " + 'Something Wrong Happened');</script>''')


@app.delete("/remove/{contact_id}", response_class=Response)
async def remove(contact_id: int, db: Session = Depends(get_db)):
    delete_contact(db, contact_id)


@app.get("/edit/{contact_id}")
async def edit(request: Request, contact_id: int, db: Session = Depends(get_db)):
    contact = read_contact(db, contact_id)
    context = {'request': request, 'contact': contact}
    return template.render('_edit.html', context)


@app.post("/edit/{contact_id}")
async def edit(request: Request, contact_id: int, fullname: str = Form(default=None), phone: int = Form(default=None), email: str = Form(default=None), db: Session = Depends(get_db)):
    if is_valid_phone(phone):
        contact = update_contact(db, contact_id=contact_id, fullname=fullname, phone=phone, email=email)
        context = {'request': request, 'contact': contact}
        return template.render('_item.html', context)
    else:
        return HTMLResponse('<script>alert("Phone number is not valid");</script>')
