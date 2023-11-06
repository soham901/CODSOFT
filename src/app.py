from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .utils import load_sub_apps, Template, Request, get_routes

app = FastAPI()

templates = Template(__package__)
load_sub_apps(app)

# Mount static files
app.mount("/static", app=StaticFiles(directory="static"), name="static")


@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.ico")


@app.get("/")
async def home(request: Request):
    nav_links = get_routes()
    return templates.render("home.html", {'request': request, 'nav_links': nav_links})

