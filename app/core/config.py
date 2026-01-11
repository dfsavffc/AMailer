from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    APP_NAME: str = "AMailer"
    DEBUG: bool = False
    
    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    SMTP_FROM_EMAIL: str
    SMTP_TIMEOUT: int = 60  # seconds
    
    MOCK_EMAIL: bool = False
    EMAIL_FOOTER: str = "Sent via AMailer - https://amailer.onrender.com/"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()