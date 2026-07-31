from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/src/static", StaticFiles(directory="src/static"), name="static")

templates = Jinja2Templates(directory="src/templates")


@app.get("/", response_class=HTMLResponse)
async def about_me_page(request: Request):
    return templates.TemplateResponse(request, "about_me.html")


@app.get("/blog/", response_class=HTMLResponse)
async def blog_page(request: Request):
    return templates.TemplateResponse(request, "blogs/home.html")


@app.get("/blog/dev", response_class=HTMLResponse)
async def blog_page(request: Request):
    return templates.TemplateResponse(request, "blogs/dev.html")


@app.get("/projects", response_class=HTMLResponse)
async def projects_page(request: Request):
    return templates.TemplateResponse(request, "projects/home.html")


@app.get("/projects/discordbots", response_class=HTMLResponse)
async def discord_bots_page(request: Request):
    return templates.TemplateResponse(request, "projects/discord_bots.html")


@app.exception_handler(404)
async def four_oh_four(request: Request, _):
    return templates.TemplateResponse(request, "errors/four_oh_four.html")
