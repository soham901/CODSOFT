# Game logic
from random import choice

CHOICES_DICT = {
    "R": "Rock",
    "P": "Paper",
    "S": "Scissors"
}
CHOICES = list(CHOICES_DICT.keys())

from fastapi import FastAPI

from src.utils import Template, Request

app = FastAPI()

score = 0

templates = Template(__package__)


@app.get("/")
async def home(request: Request):
    global score
    score = 0
    return templates.render('home.html', {'request': request})


@app.get("/play")
async def play(user_choice: str):
    global score
    computer_choice = get_computer_choice()
    result = play_game(user_choice, computer_choice)
    score = score + 2 if result == "You Win!" else score - 1 if result == "You Lose!" else score
    return {
        "user_choice": CHOICES_DICT[user_choice],
        "computer_choice": CHOICES_DICT[computer_choice],
        "result": result,
        "score": score,
    }


def play_game(user_choice: str, computer_choice: str):
    if user_choice not in CHOICES:
        return "Invalid choice!"
    if user_choice == computer_choice:
        return "Tie!"
    elif user_choice == "R":
        if computer_choice == "P":
            return "You Lose!"
        else:
            return "You Win!"
    elif user_choice == "P":
        if computer_choice == "S":
            return "You Lose!"
        else:
            return "You Win!"
    elif user_choice == "S":
        if computer_choice == "R":
            return "You Lose!"
        else:
            return "You Win!"


def get_computer_choice():
    return choice(CHOICES)
