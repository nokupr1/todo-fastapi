from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config import settings

from .database import init_db
from .routes.tasks import tasks_router

app = FastAPI(
    debug=settings.debug,
    title=settings.app_name,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=settings.static_dir), name="static")

app.include_router(tasks_router)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def root():
    return {"message": "Welcome to todo-fastapi!", "docs": "api/docs"}


@app.get("/health")
def health_check():
    return {"status": "healthy!"}
