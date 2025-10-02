import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_ADAPTER: str  # psycopg2/asyncpg

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    )
    
    def get_db_url(self) -> str:
        return (f"postgresql+{self.DB_ADAPTER}://{self.DB_USER}:{self.DB_PASSWORD}@"
        f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")


settings = Settings()
