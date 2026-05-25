# -*- coding: utf-8 -*-
"""
HISPANSHIELD â€” GUARDIAN DE PROPIEDAD INTELECTUAL
Propiedad de HispanShield (Legion de Ciberdefensa)
General Murdok (Gustavo Lobato Clara)
"""
import os, sys, socket, getpass, platform, smtplib, ssl, json, requests
from datetime import datetime, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SEAL = """
=============================================
   HISPANSHIELD â€” LEGION DE CIBERDEFENSA
   PROPIEDAD DE GENERAL MURDOK (GUSTAVO LOBATO CLARA)
   TODOS LOS DERECHOS RESERVADOS
   USO NO COMERCIAL â€” LICENSE HISPANSHIELD
=============================================
"""

SMTP_HOST = os.getenv("GUARDIAN_SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("GUARDIAN_SMTP_PORT", 587))
SMTP_USER = os.getenv("GUARDIAN_SMTP_USER", "arquitecturasiadefensamurdok@gmail.com")
SMTP_PASS = os.getenv("GUARDIAN_SMTP_PASS", "andalucia82")
NOTIFY_EMAIL = os.getenv("GUARDIAN_NOTIFY_EMAIL", "gustavolobatoclara@gmail.com")
TG_TOKEN = os.getenv("GUARDIAN_TG_TOKEN", os.getenv("TELEGRAM_TOKEN", "8690164777:AAHWAVcM4j0rf_niD0tBxATUgp9m4x-MjaQ"))
TG_CHAT_ID = os.getenv("GUARDIAN_TG_CHAT_ID", os.getenv("TELEGRAM_CHAT_ID", "1488635010"))
LOG_FILE = os.getenv("GUARDIAN_LOG", os.path.join(os.path.dirname(__file__), "guardian.log"))

def audit():
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
    except:
        hostname = "unknown"; ip = "0.0.0.0"
    return {
        "usuario": getpass.getuser(),
        "hostname": hostname,
        "ip": ip,
        "plataforma": platform.platform(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

def enviar_email(info):
    if not all([SMTP_USER, SMTP_PASS]):
        return False
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"HISPANSHIELD ALERTA â€” Acceso desde {info['hostname']}"
        msg["From"] = SMTP_USER
        msg["To"] = NOTIFY_EMAIL

        html = f"""<html><body style="font-family:monospace;">
<h2 style="color:#c00;">HISPANSHIELD â€” ALERTA DE ACCESO</h2>
<table border="1" cellpadding="8" style="border-collapse:collapse;">
<tr><td><b>Usuario</b></td><td>{info['usuario']}</td></tr>
<tr><td><b>Hostname</b></td><td>{info['hostname']}</td></tr>
<tr><td><b>IP</b></td><td>{info['ip']}</td></tr>
<tr><td><b>Plataforma</b></td><td>{info['plataforma']}</td></tr>
<tr><td><b>Timestamp</b></td><td>{info['timestamp']}</td></tr>
</table>
<p><small>General Murdok â€” HispanShield Legion de Ciberdefensa</small></p>
</body></html>"""

        msg.attach(MIMEText(html, "html"))

        ctx = ssl._create_unverified_context()
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as s:
            s.starttls(context=ctx)
            s.login(SMTP_USER, SMTP_PASS)
            s.sendmail(SMTP_USER, NOTIFY_EMAIL, msg.as_string())

        print(f"  ALERTA email enviada a {NOTIFY_EMAIL}", file=sys.stderr)
        return True
    except Exception as e:
        print(f"  Error email: {e}", file=sys.stderr)
        return False

def enviar_telegram(info):
    if not all([TG_TOKEN, TG_CHAT_ID]):
        return False
    try:
        msg = (f"*HISPANSHIELD ALERTA*\n"
               f"*Usuario:* {info['usuario']}\n"
               f"*Host:* {info['hostname']}\n"
               f"*IP:* {info['ip']}\n"
               f"*Plataforma:* {info['plataforma']}\n"
               f"*Hora:* {info['timestamp']}")
        r = requests.post(
            f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
            json={"chat_id": TG_CHAT_ID, "text": msg, "parse_mode": "Markdown"},
            timeout=15,
        )
        if r.status_code == 200:
            print("  ALERTA enviada por Telegram", file=sys.stderr)
            return True
        print(f"  Error Telegram: {r.text}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"  Error Telegram: {e}", file=sys.stderr)
        return False

def guardar_log(info):
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    except:
        pass
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(info, ensure_ascii=False) + "\n")
        print(f"  LOG guardado en {LOG_FILE}", file=sys.stderr)
    except Exception as e:
        print(f"  Error log: {e}", file=sys.stderr)

info = audit()
print(SEAL, file=sys.stderr)
print(f"  Usuario: {info['usuario']} | Host: {info['hostname']} | IP: {info['ip']}", file=sys.stderr)
guardar_log(info)
enviar_email(info)
enviar_telegram(info)
