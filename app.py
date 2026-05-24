#!/usr/bin/env python3
import os
import sys
import logging
import threading
import colorlog

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import hispan_shield_guardian  # noqa: F401
from flask import Flask, render_template
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from src.centinela.extensions import db, migrate
from src.centinela.routes import api_bp, auth_bp, telegram_bp
from src.centinela.routes.auth import init_admin
from src.centinela.routes.telegram_bot import init_telegram_bot

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    log_colors={"DEBUG": "cyan", "INFO": "green", "WARNING": "yellow", "ERROR": "red", "CRITICAL": "red,bg_white"}
))
root_logger = logging.getLogger()
root_logger.addHandler(handler)
root_logger.setLevel(logging.INFO)

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

logger = logging.getLogger("centinela")


def create_app():
    app = Flask(__name__, template_folder="src/centinela/templates", static_folder="src/centinela/static")
    app.config["SECRET_KEY"] = Config.SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = Config.DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET

    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    JWTManager(app)

    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(telegram_bp)

    with app.app_context():
        db.create_all()
        init_admin()

    @app.route("/dashboard")
    def dashboard():
        return render_template("dashboard.html")

    @app.route("/alerts")
    def alerts_page():
        return render_template("alerts.html")

    @app.route("/login")
    def login_page():
        return render_template("login.html")

    logger.info("CentinelaBot v2.0 iniciado correctamente")
    return app


app = create_app()


def start_telegram():
    if Config.check_telegram():
        logger.info("Iniciando bot de Telegram en segundo plano...")
        t = threading.Thread(target=init_telegram_bot, args=(app,), daemon=True)
        t.start()


if __name__ == "__main__":
    start_telegram()
    app.run(host="0.0.0.0", port=Config.FLASK_PORT, debug=Config.DEBUG)
