from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/src/static", StaticFiles(directory="src/static"), name="static")

templates = Jinja2Templates(directory="src/templates")


@app.get("/", response_class=HTMLResponse)
async def home_page():
    return RedirectResponse(url="/about_me")


@app.get("/about_me", response_class=HTMLResponse)
async def about_me_page(request: Request):
    return templates.TemplateResponse("about_me.html", {"request": request})


@app.get("/blog/", response_class=HTMLResponse)
async def blog_page(request: Request):
    return templates.TemplateResponse("blogs/home.html", {"request": request})


@app.get("/blog/dev", response_class=HTMLResponse)
async def blog_page(request: Request):
    return templates.TemplateResponse("blogs/dev.html", {"request": request})


@app.get("/projects", response_class=HTMLResponse)
async def projects_page(request: Request):
    return templates.TemplateResponse("projects/home.html", {"request": request})


@app.get("/projects/discordbots", response_class=HTMLResponse)
async def discord_bots_page(request: Request):
    return templates.TemplateResponse("projects/discord_bots.html", {"request": request})


@app.exception_handler(404)
async def four_oh_four(request: Request, _):
    return templates.TemplateResponse("errors/four_oh_four.html", {"request": request})
