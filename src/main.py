from typing import Optional
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.content_loader import (
    get_all_posts,
    get_post_by_slug,
    get_all_projects,
    get_featured_projects,
)

app = FastAPI(title="William Watts - Portfolio & Dev Blog")

# Static files mounting
app.mount("/src/static", StaticFiles(directory="src/static"), name="static")

templates = Jinja2Templates(directory="src/templates")


@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    featured_projects = get_featured_projects()
    latest_posts = get_all_posts()[:4]
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "active_page": "home",
            "featured_projects": featured_projects,
            "latest_posts": latest_posts,
        },
    )


@app.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    return templates.TemplateResponse(
        request,
        "about.html",
        {"active_page": "about"},
    )


@app.get("/about_me")
async def about_me_redirect():
    return RedirectResponse(url="/about", status_code=301)


@app.get("/projects", response_class=HTMLResponse)
async def projects_page(request: Request, category: Optional[str] = None):
    projects = get_all_projects(category=category)
    return templates.TemplateResponse(
        request,
        "projects/home.html",
        {
            "active_page": "projects",
            "projects": projects,
            "current_category": category,
        },
    )


@app.get("/projects/discordbots")
async def discord_bots_redirect():
    return RedirectResponse(url="/projects?category=Discord Bots", status_code=301)


@app.get("/blog", response_class=HTMLResponse)
async def blog_page(request: Request, tag: Optional[str] = None):
    all_posts = get_all_posts()
    filtered_posts = get_all_posts(tag=tag)

    # Extract unique tags across all posts
    all_tags = sorted(list({t for post in all_posts for t in post.get("tags", [])}))

    return templates.TemplateResponse(
        request,
        "blogs/home.html",
        {
            "active_page": "blog",
            "posts": filtered_posts,
            "current_tag": tag,
            "all_tags": all_tags,
        },
    )


@app.get("/blog/")
async def blog_trailing_slash_redirect():
    return RedirectResponse(url="/blog", status_code=301)


@app.get("/blog/dev")
async def blog_dev_redirect():
    return RedirectResponse(url="/blog", status_code=301)


@app.get("/blog/{slug}", response_class=HTMLResponse)
async def blog_post_page(request: Request, slug: str):
    post = get_post_by_slug(slug)
    if not post:
        return templates.TemplateResponse(
            request,
            "errors/four_oh_four.html",
            {"active_page": "blog"},
            status_code=404,
        )

    return templates.TemplateResponse(
        request,
        "blogs/post.html",
        {
            "active_page": "blog",
            "post": post,
        },
    )


@app.exception_handler(404)
async def four_oh_four(request: Request, _):
    return templates.TemplateResponse(
        request,
        "errors/four_oh_four.html",
        {"active_page": ""},
        status_code=404,
    )
