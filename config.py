import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "cambiar-en-produccion")
    JWT_SECRET = os.getenv("JWT_SECRET", "jwt-cambiar-en-produccion")
    JWT_EXPIRATION_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS", 24))

    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///centinela.db")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    AI_PROVIDER = os.getenv("AI_PROVIDER", "ollama")

    SMTP_SERVER = os.getenv("SMTP_SERVER", "")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    SMTP_USER = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    ALERT_EMAIL = os.getenv("ALERT_EMAIL", "")

    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))
    DEBUG = FLASK_ENV == "development"

    SYSLOG_HOST = os.getenv("SYSLOG_HOST", "")
    SYSLOG_PORT = int(os.getenv("SYSLOG_PORT", 514))

    @classmethod
    def check_smtp(cls):
        return all([cls.SMTP_SERVER, cls.SMTP_USER, cls.SMTP_PASSWORD, cls.ALERT_EMAIL])

    @classmethod
    def check_telegram(cls):
        return all([cls.TELEGRAM_TOKEN, cls.TELEGRAM_CHAT_ID])
