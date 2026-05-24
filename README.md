<div align="center">

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ██████╗███████╗███╗   ██╗████████╗██╗███╗   ██╗███████╗██╗      ██████╗  ██████╗ ████████╗
║  ██╔════╝██╔════╝████╗  ██║╚══██╔══╝██║████╗  ██║██╔════╝██║     ██╔═══██╗██╔═══██╗╚══██╔══╝
║  ██║     █████╗  ██╔██╗ ██║   ██║   ██║██╔██╗ ██║█████╗  ██║     ██║   ██║██║   ██║   ██║   
║  ██║     ██╔══╝  ██║╚██╗██║   ██║   ██║██║╚██╗██║██╔══╝  ██║     ██║   ██║██║   ██║   ██║   
║  ╚██████╗███████╗██║ ╚████║   ██║   ██║██║ ╚████║███████╗███████╗╚██████╔╝╚██████╔╝   ██║   
║   ╚═════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝ ╚═════╝  ╚═════╝    ╚═╝   
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

# 🛡️ CENTINELABOT
## *Plataforma SaaS de Gestión de Ciberseguridad con IA*

**Monitoreo Inteligente · Detección de Amenazas · Respuesta Automatizada**
**IA Local (Ollama) o Cloud (OpenAI) · Dashboard en Tiempo Real · Bot Telegram**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-000000?style=for-the-badge&logo=llama&logoColor=white)](https://ollama.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](#-despliegue-con-docker)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![CI](https://img.shields.io/github/actions/workflow/status/murdok1982/CentinelaBot/ci.yml?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/murdok1982/CentinelaBot/actions)
[![Stars](https://img.shields.io/github/stars/murdok1982/CentinelaBot?style=for-the-badge&logo=github)](https://github.com/murdok1982/CentinelaBot)

</div>

---

## 🌟 ¿Qué es CentinelaBot?

**CentinelaBot** es una plataforma completa de **ciberseguridad como servicio (SaaS)** que integra inteligencia artificial, detección de amenazas en tiempo real, gestión de alertas multicanal y un dashboard visual impactante — todo corriendo **en tu infraestructura**, con **IA local gratuita** o en la nube.

```
                🧠 AI ANALYZER
               (Ollama / OpenAI)
                      │
    ┌─────────────────┼─────────────────┐
    │                 │                 │
    ▼                 ▼                 ▼
┌────────┐     ┌──────────┐     ┌──────────┐
│🔍 THREAT│────▶│🚨 ALERT  │────▶│📊 DASHBOARD│
│DETECTOR│     │ MANAGER  │     │  CHART.JS │
└────────┘     └──────────┘     └──────────┘
    │                 │                 │
    ▼                 ▼                 ▼
┌────────┐     ┌──────────┐     ┌──────────┐
│🔗 SIEM  │     │📧 EMAIL  │     │🤖 TELEGRAM│
│ SYSLOG  │     │  SMTP    │     │   BOT    │
└────────┘     └──────────┘     └──────────┘
```

---

## 🎯 Lo que lo hace diferente

| 🚀 Prestación | 🔥 CentinelaBot | 😢 Otros |
|---|---|---|
| **IA 100% local y gratis** | Ollama integrado — sin API keys, sin costos | Suelen requerir OpenAI sí o sí |
| **Detección real de amenazas** | 8 tipos con regex + análisis IA | Muchos usan datos fake/random |
| **Base de datos persistente** | SQLite (dev) / PostgreSQL (prod) | En memoria — se pierde al reiniciar |
| **Dashboard visual impactante** | Chart.js + tema oscuro profesional | Solo JSON o CLI |
| **Alertas multicanal** | Email SMTP + Telegram + Dashboard web | Un solo canal |
| **Autenticación y roles** | JWT + bcrypt + admin/analyst | Sin autenticación |
| **Docker con PostgreSQL** | `docker-compose up` y listo | Sin Docker o solo Flask solo |
| **Bot de Telegram interactivo** | `/status`, `/alerts`, `/stats` | No tienen bot |
| **Forwarding SIEM** | Syslog, Splunk, ELK | No exportan eventos |
| **Tests automatizados** | 19 tests, CI/CD, linting | Sin tests |

---

## 💰 Apoya Este Proyecto

<div align="center">

### ¡Donaciones en Bitcoin Bienvenidas!

[![Bitcoin](https://img.shields.io/badge/Bitcoin-000000?style=for-the-badge&logo=bitcoin&logoColor=white)](https://bitcoin.org)

```
┌──────────────────────────────────────────────────┐
│             ₿ BTC Donation Address ₿              │
├──────────────────────────────────────────────────┤
│                                                  │
│  bc1qqphwht25vjzlptwzjyjt3sex7e3p8twn390fkw     │
│                                                  │
│  Network: Bitcoin (BTC)                          │
│                                                  │
│  Escanea el QR desde tu wallet:                  │
└──────────────────────────────────────────────────┘
```

![Bitcoin QR](https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=bitcoin:bc1qqphwht25vjzlptwzjyjt3sex7e3p8twn390fkw)

**Dirección:** `bc1qqphwht25vjzlptwzjyjt3sex7e3p8twn390fkw`

*¡Apoya el desarrollo de herramientas de ciberseguridad open-source!* 🙏

</div>

---

## ✨ Características en Detalle

### 🧠 AI Analyzer — Inteligencia Artificial para Ciberseguridad

| Proveedor | Tipo | Costo | Privacidad |
|---|---|---|---|
| **Ollama** (LLaMA 3, Mistral, CodeLLaMA) | Local | ✅ Gratis | ✅ 100% privado |
| **OpenAI GPT** (3.5/4) | Cloud | 💲 API key | ⚠️ Datos viajan |

```python
# El analizador elige automáticamente según tu config
AI_PROVIDER=ollama    # IA local sin costo
# o
AI_PROVIDER=openai    # OpenAI GPT si prefieres
OPENAI_API_KEY=sk-...
```

✔️ Clasifica severidad: `low` · `medium` · `high` · `critical`  
✔️ Genera recomendaciones de respuesta  
✔️ Fallback inteligente cuando la IA no responde

---

### 🔍 Threat Detector — Motor de Detección

**8 tipos de amenazas detectadas con patrones reales:**

| Tipo | Regex | Severidad |
|---|---|---|
| 🔍 **Port Scan** | `nmap`, `masscan`, `syn scan` | Baja |
| 🔑 **Brute Force** | `failed login`, `auth fail` | Media |
| 🦠 **Malware** | `trojan`, `ransomware`, `backdoor` | Alta |
| 🚪 **Intrusion** | `CVE-`, `exploit`, `unauthorized` | Crítica |
| 🎣 **Phishing** | `phish`, `spoof`, `fake login` | Alta |
| 🌊 **DDoS** | `flood`, `amplification` | Crítica |
| 📤 **Data Exfil** | `exfil`, `data leak`, `dns tunnel` | Crítica |
| 🕵️ **Recon** | `whois`, `dns enum`, `dir bust` | Baja |

✔️ Ingesta de logs vía API  
✔️ Almacenamiento persistente en BD  
✔️ Estadísticas por tipo y severidad

---

### 🚨 Alert Manager — Gestión de Alertas Multicanal

```
Evento detectado → IA analiza → ¿Crítico/Alto? 
                                  ↓
                    ┌──────────────────────┐
                    │   NOTIFICACIONES      │
                    ├──────────────────────┤
                    │ 📧 Email SMTP        │
                    │ 🤖 Telegram Bot      │
                    │ 📊 Dashboard Web     │
                    └──────────────────────┘
```

✔️ Estados: `active` → `investigating` → `resolved`  
✔️ Resolución desde API o dashboard  
✔️ Historial completo en base de datos

---

### 📊 Dashboard Web — Panel de Control

```
┌─────────────────────────────────────────────────────────────┐
│  🛡️ CENTINELABOT                  [🟢 Sistema Operativo]    │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │⚠️ 12     │  │🚨 3      │  │📊 1,234  │  │🔒 85/100│       │
│  │Amenazas │  │Alertas  │  │Eventos  │  │Score    │        │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘        │
├─────────────────────────────────────────────────────────────┤
│  📊 Distribución                📊 Severidad                │
│  [Gráfico Doughnut]             [Gráfico Barras]           │
├─────────────────────────────────────────────────────────────┤
│  🧠 AI Analyzer 🟢   🔍 Threat Detector 🟢                 │
│  🚨 Alert Manager 🟢  🔗 SIEM 🟢  📊 Dashboard 🟢          │
└─────────────────────────────────────────────────────────────┘
```

✔️ **Tema oscuro** profesional tipo SOC  
✔️ **Gráficos interactivos** con Chart.js  
✔️ **Security Score** dinámico basado en datos reales  
✔️ **Health check** visual de cada módulo

---

### 🔗 SIEM Integration — Integración con SIEM

✔️ Almacenamiento de eventos con consultas por tipo/severidad/origen  
✔️ **Forwarding a syslog** (Splunk, ELK, rsyslog, Graylog)  
✔️ API REST para consulta y filtrado

---

### 🤖 Telegram Bot — Monitoreo desde tu Móvil

Configura tu bot en 2 minutos:

```bash
# En .env:
TELEGRAM_TOKEN=123456:ABC-DEF1234ghIkl
TELEGRAM_CHAT_ID=123456789
```

| Comando | Qué hace |
|---|---|
| `/start` | Información del bot |
| `/status` | Estado del sistema, amenazas, score |
| `/alerts` | Últimas alertas activas |

Además recibe **notificaciones push** cuando se detectan amenazas críticas.

---

## 📦 Instalación

### 🏁 Rápida (local — 2 minutos)

```bash
# 1. Clonar
git clone https://github.com/murdok1982/CentinelaBot.git
cd CentinelaBot

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar (opcional — valores por defecto funcionan)
cp .env.example .env

# 4. ¡Iniciar!
python app.py
```

Abre **[http://localhost:5000](http://localhost:5000)** 🚀

> 🔑 **Credenciales por defecto:** `admin` / `admin123`

---

### 🐳 Producción con Docker (recomendado)

Lanza todo el ecosistema con un solo comando:

```bash
docker-compose up -d
```

Esto inicia:
- **CentinelaBot** → `http://localhost:5000`
- **PostgreSQL 16** → Base de datos relacional
- **Ollama** → Motor de IA local

Primera vez — descarga el modelo LLM:
```bash
docker exec centinela-ollama ollama pull llama3.1
```

---

### ☁️ Usar solo OpenAI (sin Ollama)

Edita `.env`:
```env
AI_PROVIDER=openai
OPENAI_API_KEY=sk-tu-api-key-aqui
```

---

## 🎮 API Reference

### 📡 Endpoints principales

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `GET` | `/` | ❌ | Info del sistema |
| `GET` | `/api/health` | ❌ | Health check |
| `GET` | `/api/dashboard` | ❌ | Dashboard data |
| `GET` | `/api/threats` | ❌ | Amenazas detectadas |
| `GET` | `/api/alerts` | ❌ | Alertas activas |
| `POST` | `/api/alerts/<id>/resolve` | ❌ | Resolver alerta |
| `GET` | `/api/events` | ❌ | Eventos (con filtros) |
| `POST` | `/api/analyze` | ❌ | Analizar evento con IA |
| `POST` | `/api/ingest` | ❌ | Ingerir log (detección) |
| `GET` | `/api/stats` | ❌ | Estadísticas completas |
| `POST` | `/api/auth/login` | ❌ | Login JWT |
| `POST` | `/api/auth/register` | ❌ | Registrar usuario |
| `GET` | `/api/auth/me` | ✅ | Perfil del usuario |

### 💻 Ejemplos con curl

```bash
# 🩺 Health check
curl http://localhost:5000/api/health

# 📊 Dashboard
curl http://localhost:5000/api/dashboard

# 🧠 Analizar evento con IA
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"event_type":"malware","source":"firewall","description":"Posible malware detectado en endpoint"}'

# 📥 Ingerir log (detecta amenazas automáticamente)
curl -X POST http://localhost:5000/api/ingest \
  -H "Content-Type: application/json" \
  -d '{"raw":"Failed login attempt from 192.168.1.100","source":"ssh"}'

# 🔐 Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# 🚨 Alertas activas
curl http://localhost:5000/api/alerts

# ✅ Resolver alerta
curl -X POST http://localhost:5000/api/alerts/ALT-1001/resolve

# 📈 Estadísticas
curl http://localhost:5000/api/stats
```

---

## 🗺️ Arquitectura del Proyecto

```
CentinelaBot/
│
├── 🚀 app.py                      # Entry point — Inicializa Flask + módulos
├── ⚙️ config.py                   # Configuración centralizada (desde .env)
├── 📦 requirements.txt            # Dependencias Python
├── 🐳 Dockerfile                  # Construcción Docker multi-etapa
├── 🐳 docker-compose.yml          # Orquestación: app + PostgreSQL + Ollama
├── 📄 .env.example                # Template de configuración
├── 🔄 ci.yml                      # GitHub Actions (tests + build)
│
├── 📁 src/
│   └── 📁 centinela/
│       ├── 📄 __init__.py
│       ├── 📄 extensions.py       # Flask-SQLAlchemy, Flask-Migrate
│       │
│       ├── 📁 models/             # Modelos de BD
│       │   ├── 📄 user.py         # 👤 Usuarios (username, email, rol, bcrypt)
│       │   ├── 📄 alert.py        # 🚨 Alertas persistentes
│       │   └── 📄 event.py        # 📋 Eventos de seguridad
│       │
│       ├── 📁 services/           # 🔧 Lógica de negocio
│       │   ├── 📄 ai_analyzer.py      # 🧠 IA: Ollama + OpenAI + fallback
│       │   ├── 📄 threat_detector.py  # 🔍 Detección por 8 patrones regex
│       │   ├── 📄 alert_manager.py    # 🚨 Alertas + Email SMTP + Telegram
│       │   ├── 📄 siem_integration.py # 🔗 Forwarding syslog + consultas
│       │   └── 📄 dashboard_service.py # 📊 Datos reales + security score
│       │
│       ├── 📁 routes/             # 🌐 Endpoints REST
│       │   ├── 📄 api.py          # 15 endpoints REST
│       │   ├── 📄 auth.py         # 🔐 JWT login/register/me
│       │   └── 📄 telegram_bot.py # 🤖 Bot Telegram (polling)
│       │
│       ├── 📁 templates/          # 🎨 Frontend
│       │   ├── 📄 base.html       # Layout base (navbar, CSS, Chart.js)
│       │   ├── 📄 dashboard.html  # Panel con gráficos + stats
│       │   ├── 📄 alerts.html     # Tabla de alertas con filtros
│       │   └── 📄 login.html      # Login con JWT
│       │
│       └── 📁 static/
│           ├── 📁 css/
│           │   └── 📄 style.css   # Tema oscuro profesional SOC
│           └── 📁 js/
│               └── 📄 dashboard.js # Chart.js + fetch + filters
│
├── 📁 tests/                      # ✅ Tests automatizados
│   ├── 📄 conftest.py             # Fixtures (app test, client, auth)
│   ├── 📄 test_api.py             # 17 tests de endpoints REST
│   └── 📄 test_threat_detector.py # 2 tests de detección de amenazas
│
└── 📄 hispan_shield_guardian.py   # 🛡️ Módulo de auditoría (autor)
```

---

## 🧪 Tests

```bash
pip install pytest-cov httpx
python -m pytest tests/ -v --cov=src
```

```
tests/test_api.py ................. ✅ 17 passed
tests/test_threat_detector.py ... ✅ 2 passed
═══════════════════════════════════════
Total: 19 passed 🎉
═══════════════════════════════════════
```

---

## 🛣️ Roadmap

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ COMPLETADO (v2.0)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • Flask API REST con 15+ endpoints
  • Base de datos SQLite / PostgreSQL
  • Autenticación JWT con bcrypt + roles
  • AI Analyzer: Ollama + OpenAI + fallback
  • Threat Detector: 8 patrones regex
  • Alert Manager: Email + Telegram + Dashboard
  • Dashboard Chart.js con tema oscuro
  • SIEM Integration con syslog forwarding
  • Bot de Telegram interactivo
  • Docker Compose multi-servicio
  • CI/CD con GitHub Actions
  • 19 tests automatizados

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🔜 PRÓXIMOS PASOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • 🔎 Escaneo de vulnerabilidades con Nmap integrado
  • 🌍 Threat Intelligence: VirusTotal, Shodan, AlienVault OTX
  • 📄 Generación de reportes PDF
  • ⚡ WebSockets para dashboard en tiempo real
  • 🏢 Multi-tenencia con organizaciones
  • 📱 App móvil (Flutter) para monitoreo
```

---

## ⚖️ Licencia

<div align="center">

**MIT License** — Copyright © 2026 murdok1982

*El software se proporciona "TAL CUAL", sin garantía de ningún tipo.*

[Ver licencia completa →](LICENSE)

---

### ⭐ ¿Te sirve? ¡Deja una estrella en GitHub!

**"Protege tu infraestructura, no solo tus datos."** 🛡️

--- 

<p align="center">
  <a href="https://github.com/murdok1982/CentinelaBot">GitHub</a> •
  <a href="https://github.com/murdok1982">@murdok1982</a> •
  <a href="https://www.linkedin.com/in/gustavo-lobato-clara-2b446b102/">LinkedIn</a>
</p>

</div>
