from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Mongo App"
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB: str = "fast_api"
    JWT_SECRET: str = "fast_api"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
