from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    OPENAI_API_KEY:str

    OPENAI_MODEL: str = "gpt-5"

    GEMINI_API_KEY:str

    GEMINI_MODEL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

settings = Settings()