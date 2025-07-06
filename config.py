from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    MODEL_PATH: str = "yolov10n.pt"
    MODEL_CONFIDENCE: float = 0.5
    CLASSES_OF_INTEREST: list[int] = [0, 2]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()