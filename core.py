from pydantic import BaseSettings


class Settings(BaseSettings):
    TELEGRAM_TOKEN: str
    CLIENT_KEY: str
    CLIENT_SECRET: str
    API_HOST: str

    class Config:
        env_file = ".env"
        case_sensetive = False


settings = Settings()
