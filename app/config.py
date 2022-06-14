from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str = "localhost"
    database_port: str = 5432
    database_password: str = "secure123"
    database_name: str = "users_api"
    database_username: str = "postgres"

    class Config:
        env_file = ".env"


settings = Settings()
