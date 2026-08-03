from pathlib import Path
import json
import math
from typing import Dict, List, Optional
import frontmatter
import markdown

BASE_DIR = Path(__file__).resolve().parent
POSTS_DIR = BASE_DIR / "content" / "posts"
PROJECTS_FILE = BASE_DIR / "content" / "projects.json"


def get_markdown_renderer() -> markdown.Markdown:
    return markdown.Markdown(
        extensions=[
            "fenced_code",
            "codehilite",
            "tables",
            "toc",
            "attr_list",
        ],
        extension_configs={
            "codehilite": {
                "css_class": "highlight",
                "use_pygments": True,
                "noclasses": False,
            }
        },
    )


def calculate_read_time(text: str) -> int:
    words = len(text.split())
    minutes = math.ceil(words / 200)
    return max(1, minutes)


def get_all_posts(tag: Optional[str] = None) -> List[Dict]:
    if not POSTS_DIR.exists():
        return []

    posts = []
    for file_path in POSTS_DIR.glob("*.md"):
        try:
            post = frontmatter.load(file_path)
            if not post.metadata.get("published", True):
                continue

            slug = file_path.stem
            read_time = calculate_read_time(post.content)

            posts.append(
                {
                    "slug": slug,
                    "title": post.metadata.get("title", slug.replace("-", " ").title()),
                    "date": str(post.metadata.get("date", "2026-01-01")),
                    "description": post.metadata.get("description", ""),
                    "tags": post.metadata.get("tags", []),
                    "read_time": f"{read_time} min read",
                    "featured": post.metadata.get("featured", False),
                }
            )
        except Exception as e:
            print(f"Error parsing post {file_path}: {e}")

    # Sort posts by date descending
    posts.sort(key=lambda p: p["date"], reverse=True)

    if tag:
        tag_lower = tag.lower()
        posts = [p for p in posts if tag_lower in [t.lower() for t in p["tags"]]]

    return posts


def get_post_by_slug(slug: str) -> Optional[Dict]:
    file_path = POSTS_DIR / f"{slug}.md"
    if not file_path.exists():
        return None

    try:
        post = frontmatter.load(file_path)
        if not post.metadata.get("published", True):
            return None

        md = get_markdown_renderer()
        html_content = md.convert(post.content)
        read_time = calculate_read_time(post.content)

        return {
            "slug": slug,
            "title": post.metadata.get("title", slug.replace("-", " ").title()),
            "date": str(post.metadata.get("date", "")),
            "description": post.metadata.get("description", ""),
            "tags": post.metadata.get("tags", []),
            "read_time": f"{read_time} min read",
            "content": html_content,
            "toc": getattr(md, "toc", ""),
        }
    except Exception as e:
        print(f"Error reading post {slug}: {e}")
        return None


def get_all_projects(category: Optional[str] = None) -> List[Dict]:
    if not PROJECTS_FILE.exists():
        return []

    try:
        with open(PROJECTS_FILE, "r", encoding="utf-8") as f:
            projects = json.load(f)

        if category and category.lower() != "all":
            cat_lower = category.lower()
            projects = [
                p
                for p in projects
                if cat_lower in [t.lower() for t in p.get("tags", [])]
                or cat_lower == p.get("category", "").lower()
            ]

        return projects
    except Exception as e:
        print(f"Error reading projects: {e}")
        return []


def get_featured_projects() -> List[Dict]:
    projects = get_all_projects()
    return [p for p in projects if p.get("featured", False)]
