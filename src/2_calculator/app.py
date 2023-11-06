from fastapi import FastAPI, Request,  Form

from fastapi.responses import HTMLResponse

from src.utils import Template

app = FastAPI()

template = Template(__package__)

ans = None


@app.get("/")
async def home(request: Request):
    global ans
    return template.render("home.html", {'request': request, 'ans': ans})


@app.post("/")
async def calc(expression: str = Form(...)):
    res = HTMLResponse('<span>Error</span>')
    try:
        res = eval(expression)
    except Exception as e:
        pass
    return res
