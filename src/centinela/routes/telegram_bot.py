import logging
from flask import Blueprint, jsonify
from config import Config
from src.centinela.services import AlertManager

logger = logging.getLogger("centinela.telegram")
telegram_bp = Blueprint("telegram", __name__)


def init_telegram_bot(app):
    if not Config.check_telegram():
        logger.info("Telegram bot no configurado (falta token o chat_id)")
        return

    try:
        from telegram import Update
        from telegram.ext import Application, CommandHandler, ContextTypes

        application = Application.builder().token(Config.TELEGRAM_TOKEN).build()

        async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await update.message.reply_text(
                "CentinelaBot activo.\n"
                "Comandos:\n"
                "/status - Estado del sistema\n"
                "/alerts - Alertas activas\n"
                "/stats - Estadisticas"
            )

        async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
            with app.app_context():
                from src.centinela.services.dashboard_service import DashboardService
                dash = DashboardService()
                s = dash.get_summary()
                msg = (
                    f"Estado: {s['system_status']}\n"
                    f"Amenazas: {s['statistics']['threats_detected_today']}\n"
                    f"Alertas activas: {s['statistics']['alerts_active']}\n"
                    f"Security Score: {s['statistics']['security_score']}/100"
                )
            await update.message.reply_text(msg)

        async def cmd_alerts(update: Update, context: ContextTypes.DEFAULT_TYPE):
            with app.app_context():
                mgr = AlertManager()
                a = mgr.get_active_alerts()
            if a["total"] == 0:
                await update.message.reply_text("No hay alertas activas.")
                return
            lines = [f"{a['severity']} | {a['title']}" for a in a["alerts"][:5]]
            await update.message.reply_text(
                f"Alertas activas ({a['total']}):\n" + "\n".join(lines)
            )

        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("status", cmd_status))
        application.add_handler(CommandHandler("alerts", cmd_alerts))

        application.run_polling(drop_pending_updates=True)

    except Exception as e:
        logger.error("Telegram bot init error: %s", e)


@telegram_bp.route("/api/telegram/webhook", methods=["POST"])
def webhook():
    return jsonify({"status": "telegram webhook endpoint"})
