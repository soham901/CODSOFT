import secrets

from fastapi import FastAPI, Request, Form
from src.utils import Template

app = FastAPI()

template = Template(__package__)


@app.get("/")
async def home(request: Request):
    return template.render("home.html", {'request': request})


@app.post("/generate")
async def generate(
        length: int = Form(...),
        uppercase: bool = Form(default=False),
        lowercase: bool = Form(default=False),
        numbers: bool = Form(default=False),
        symbols: bool = Form(default=False),
        exclude: str = Form(default=''),
):
    try:
        return generate_password(length, uppercase, lowercase, numbers, symbols, exclude)
    except Exception as e:
        print(e)
        return str(e)


def generate_password(length: int, uppercase: bool, lowercase: bool, numbers: bool, symbols: bool, exclude: str):
    """ generate a strong password with given parameters """
    if length < 8:
        raise ValueError("Password must be at least 8 characters long.")

    if length > 32:
        raise ValueError("Password must be at most 32 characters long.")

    if not (uppercase or lowercase or numbers or symbols):
        raise ValueError("Password must contain at least one of the following: uppercase, lowercase, numbers, symbols.")

    character_set = ""
    if uppercase:
        character_set += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if lowercase:
        character_set += "abcdefghijklmnopqrstuvwxyz"
    if numbers:
        character_set += "0123456789"
    if symbols:
        character_set += "!@#$%^&*()"

    for character in exclude:
        character_set = character_set.replace(character, "")

    password = ""
    for i in range(length):
        password += secrets.choice(character_set)

    return password
