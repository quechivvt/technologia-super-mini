from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    REDIS_HOST: str = "redis"

    REDIS_PORT: int = 6379

    REDIS_DB: int = 0

    USER_SERVICE_GRPC_HOST: str = "user-service"

    USER_SERVICE_GRPC_PORT: int = 50051

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()