from .api import api_bp
from .auth import auth_bp
from .telegram_bot import telegram_bp

__all__ = ["api_bp", "auth_bp", "telegram_bp"]
