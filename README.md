<div align="center">

# 🛡️ CentinelaBot v2.0

### *Plataforma SaaS de Gestión de Ciberseguridad con IA*

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue?logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-000?logo=llama&logoColor=white)](https://ollama.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-Compatible-412991?logo=openai&logoColor=white)](https://openai.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](#-despliegue-con-docker)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Monitoreo · Detección · Respuesta Automatizada · IA Local o Cloud**

</div>

---

## 🔥 ¿Qué es CentinelaBot?

CentinelaBot es una **plataforma SaaS de ciberseguridad** que unifica:

```
┌──────────────────────────────────────────────────────────┐
│                    CENTINELABOT                          │
├──────────────────────────────────────────────────────────┤
│  🧠 AI Analyzer    🔍 Threat Detector   🚨 Alert Manager │
│  📊 Dashboard       🔗 SIEM Integration  🤖 Telegram Bot │
│  🔐 Autenticación   🗄️ Base de Datos     🐳 Docker        │
└──────────────────────────────────────────────────────────┘
```

### ¿Qué lo hace diferente?

| Característica | CentinelaBot |
|---|---|
| **IA local sin costo** | Usa Ollama (LLaMA 3, Mistral) — 100% gratis, 100% privado |
| **IA en la nube** | También compatible con OpenAI GPT si prefieres |
| **Persistencia real** | SQLite para dev, PostgreSQL para producción |
| **Detección real** | Analiza logs con patrones de amenazas reales (no datos fake) |
| **Múltiples canales de alerta** | Email SMTP + Telegram + Dashboard |
| **Forwarding SIEM** | Envía eventos a syslog externo, Splunk, ELK |
| **Autenticación JWT** | Login seguro con roles (admin, analyst) |
| **Dashboard visual** | Gráficos en tiempo real con Chart.js |
| **Docker listo** | `docker-compose up` y ya funciona |
| **Bot de Telegram** | Consulta el estado desde Telegram |

---

## ✨ Características

### 🧠 AI Analyzer
- Analiza eventos de seguridad con **LLMs locales (Ollama)** o **OpenAI GPT**
- Clasifica severidad (low/medium/high/critical)
- Genera recomendaciones de respuesta automáticas
- Fallback inteligente cuando la IA no está disponible

### 🔍 Threat Detector
- **Detección basada en patrones** con expresiones regulares
- Tipos detectados: port_scan, brute_force, malware, intrusion, phishing, ddos, data_exfil, recon
- Ingesta de logs en tiempo real
- Almacenamiento persistente en base de datos

### 🚨 Alert Manager
- Alertas persistentes con estados (active, investigating, resolved)
- Notificaciones multicanal: **Email SMTP** + **Telegram**
- Resolución de alertas vía API

### 📊 Dashboard
- **Gráficos interactivos** con Chart.js (distribución de amenazas, severidad)
- Estadísticas en tiempo real
- Security Score dinámico
- Health check visual de módulos
- **Tema oscuro** profesional

### 🔗 SIEM Integration
- Almacenamiento de eventos con filtros y consultas
- **Forwarding a syslog externo** (Splunk, ELK, rsyslog)
- API de consulta de eventos

### 🤖 Telegram Bot
- Comandos: `/status`, `/alerts`, `/stats`
- Notificaciones de alertas críticas en tiempo real
- Funciona en segundo plano con Flask

---

## 📥 Instalación

### Rápida (local)

```bash
# 1. Clonar
git clone https://github.com/murdok1982/CentinelaBot.git
cd CentinelaBot

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar entorno
cp .env.example .env
# Edita .env si quieres cambiar IA, email, telegram, etc.

# 4. Iniciar
python app.py
```

Abre **http://localhost:5000** en tu navegador.

> Login: `admin` / `admin123`

### Con Docker (recomendado para producción)

```bash
# Lanza CentinelaBot + PostgreSQL + Ollama
docker-compose up -d

# Espera a que Ollama descargue el modelo (primera vez)
docker exec centinela-ollama ollama pull llama3.1

# Abre http://localhost:5000
```

### Sin Ollama (usando solo OpenAI)

Edita `.env`:

```env
AI_PROVIDER=openai
OPENAI_API_KEY=sk-tu-api-key
```

---

## 🎮 Uso

### Dashboard Web

| Ruta | Descripción |
|---|---|
| `/dashboard` | Panel principal con gráficos |
| `/alerts` | Tabla de alertas con filtros |
| `/login` | Login con JWT |
| `/api/health` | Health check JSON |

### API REST

```bash
# Health check
curl http://localhost:5000/api/health

# Dashboard
curl http://localhost:5000/api/dashboard

# Analizar evento con IA
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"event_type":"malware","source":"firewall","description":"Posible malware detectado"}'

# Ingerir log (detecta amenazas automáticamente)
curl -X POST http://localhost:5000/api/ingest \
  -H "Content-Type: application/json" \
  -d '{"raw":"Failed login attempt from 192.168.1.100","source":"ssh"}'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Alertas
curl http://localhost:5000/api/alerts

# Resolver alerta
curl -X POST http://localhost:5000/api/alerts/ALT-1001/resolve

# Estadísticas
curl http://localhost:5000/api/stats
```

### Telegram Bot

Configura en `.env`:
```env
TELEGRAM_TOKEN=tu-token-de-botfather
TELEGRAM_CHAT_ID=tu-chat-id
```

Luego en Telegram:
```
/start        → Info del bot
/status       → Estado del sistema
/alerts       → Alertas activas
```

---

## 🗺️ Arquitectura

```
CentinelaBot/
├── app.py                          # Entry point Flask
├── config.py                       # Configuración centralizada
├── requirements.txt                # Dependencias
├── Dockerfile                      # Construcción Docker
├── docker-compose.yml              # Orquestación multi-servicio
├── .env.example                    # Template de entorno
├── ci.yml                          # GitHub Actions CI/CD
│
├── src/
│   └── centinela/
│       ├── __init__.py
│       ├── extensions.py           # Flask-SQLAlchemy, Migrate
│       ├── models/
│       │   ├── user.py             # Usuarios y roles
│       │   ├── alert.py            # Alertas persistentes
│       │   └── event.py            # Eventos de seguridad
│       ├── services/
│       │   ├── ai_analyzer.py      # Ollama + OpenAI + fallback
│       │   ├── threat_detector.py  # Detección por patrones regex
│       │   ├── alert_manager.py    # Alertas + Email + Telegram
│       │   ├── siem_integration.py # Syslog forwarding + consultas
│       │   └── dashboard_service.py # Datos reales del dashboard
│       ├── routes/
│       │   ├── api.py              # Endpoints REST
│       │   ├── auth.py             # Registro, login JWT
│       │   └── telegram_bot.py     # Bot de Telegram
│       ├── templates/
│       │   ├── base.html           # Layout base
│       │   ├── dashboard.html      # Panel con Chart.js
│       │   ├── alerts.html         # Tabla de alertas
│       │   └── login.html          # Pantalla de login
│       └── static/
│           ├── css/style.css       # Tema oscuro profesional
│           └── js/dashboard.js     # Lógica del frontend
│
├── tests/
│   ├── conftest.py                 # Fixtures (app, client, auth)
│   ├── test_api.py                 # Tests de endpoints
│   └── test_threat_detector.py     # Tests de detección
│
└── hispan_shield_guardian.py       # Módulo de auditoría
```

---

## 🧪 Tests

```bash
pip install pytest-cov httpx
python -m pytest tests/ -v --cov=src
```

```
test_api.py ................. 17 passed
test_threat_detector.py ...  3 passed
```

---

## 🧠 Roadmap

| Estado | Funcionalidad |
|---|---|
| ✅ | Flask API REST con 15+ endpoints |
| ✅ | Base de datos SQLite/PostgreSQL |
| ✅ | Autenticación JWT con roles |
| ✅ | AI Analyzer (Ollama + OpenAI) |
| ✅ | Threat Detector con patrones reales |
| ✅ | Alert Manager multicanal (Email + Telegram) |
| ✅ | Dashboard con Chart.js (tema oscuro) |
| ✅ | SIEM Integration con syslog forwarding |
| ✅ | Bot de Telegram interactivo |
| ✅ | Docker Compose multi-servicio |
| ✅ | CI/CD con GitHub Actions |
| 🔜 | Escaneo de vulnerabilidades con Nmap |
| 🔜 | Integración con VirusTotal, Shodan, AlienVault OTX |
| 🔜 | Módulo de reportes PDF |
| 🔜 | WebSockets para dashboard en tiempo real |
| 🔜 | Multi-tenencia (organizaciones) |

---

## ⚖️ Licencia

**MIT License** — Ver [LICENSE](LICENSE).

---

<div align="center">

### ⭐ ¿Te sirve? ¡Deja una estrella!

**Protege tu infraestructura. 🛡️**

</div>
