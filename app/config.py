from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql://incident_user:incident_pass@localhost:5432/incidents"
    log_level: str = "INFO"


settings = Settings()
