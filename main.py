import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware

from app.services.database import init_db
from app.routes import pages, auth, planners, session

BASE_DIR=Path(__file__).resolve().parent
app=FastAPI(title="PocketSmart AI", version="1.0.0")
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY","dev-secret-change-me"), max_age=60*60*24*7)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.mount("/static",StaticFiles(directory=BASE_DIR/"static"),name="static")
app.state.templates=Jinja2Templates(directory=BASE_DIR/"templates")
init_db()

app.include_router(pages.router)
app.include_router(auth.router)
app.include_router(planners.router)
app.include_router(session.router)

@app.on_event("startup")
async def startup():
    init_db()

@app.get("/startup")
async def startup_check():
    return {"status":"ok","service":"PocketSmart AI"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000"))
    )