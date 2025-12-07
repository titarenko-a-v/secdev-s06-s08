
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from starlette.status import HTTP_401_UNAUTHORIZED

from .models import LoginRequest
from .db import query, query_one

app = FastAPI(title="secdev-seed-s06-s08")

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@app.get("/", response_class=HTMLResponse)
def index(request: Request, msg: str | None = None):
    return templates.TemplateResponse({"request": request, "message": msg or "Hello!"}, "index.html")

@app.get("/echo", response_class=HTMLResponse)
def echo(request: Request, msg: str | None = None):
    return templates.TemplateResponse({"request": request, "message": msg or ""}, "index.html")

@app.get("/search")
def search(q: str | None = None):
    if q:
        sql = "SELECT id, name, description FROM items WHERE name LIKE ?"
        params = (f"%{q}%",)
    else:
        sql = "SELECT id, name, description FROM items LIMIT 10"
        params = ()

    return JSONResponse(content={"items": query(sql, params)})


@app.post("/login")
def login(payload: LoginRequest):
    sql = "SELECT id, username FROM users WHERE username = ? AND password = ?"

    user_data = query_one(sql, (payload.username, payload.password))
    if not user_data:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return {"status": "ok", "user": user_data["username"], "token": "dummy"}
