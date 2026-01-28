from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GROQ_API_KEY: str
    DATABASE_URL: str = "sqlite:///./brain_platform.db"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
