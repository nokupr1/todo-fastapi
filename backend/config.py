from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "todo-app"
    debug: bool = True
    database_url: str = "sqlite:///./todo.db"
    cors_origins: list = [
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://localhost:3000",
    ]

    class Config:
        env_file = ".env"


settings = Settings()
