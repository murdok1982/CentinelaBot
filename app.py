#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CentinelaBot - SaaS de Gestión de Ciberseguridad con IA
Autor: murdok1982
Licencia: MIT
"""

import os
import logging
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import colorlog
from datetime import datetime
import json

from modules.ai_analyzer import AIAnalyzer
from modules.threat_detector import ThreatDetector
from modules.alert_manager import AlertManager
from modules.siem_integration import SIEMIntegration
from modules.dashboard_data import DashboardData

# Configuración de logging con colores
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }
))

logger = colorlog.getLogger('CentinelaBot')
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Cargar variables de entorno
load_dotenv()

# Inicializar Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
CORS(app)

# Inicializar módulos
ai_analyzer = AIAnalyzer()
threat_detector = ThreatDetector()
alert_manager = AlertManager()
siem = SIEMIntegration()
dashboard = DashboardData()

logger.info('🛡️ CentinelaBot iniciado correctamente')


@app.route('/')
def index():
    """Página principal"""
    return jsonify({
        'app': 'CentinelaBot',
        'version': '1.0.0',
        'status': 'running',
        'message': '🛡️ Sistema de Gestión de Ciberseguridad con IA activo',
        'endpoints': {
            '/': 'Información del sistema',
            '/api/dashboard': 'Datos del dashboard',
            '/api/threats': 'Amenazas detectadas',
            '/api/analyze': 'Analizar evento con IA',
            '/api/alerts': 'Alertas activas',
            '/api/health': 'Estado del sistema'
        }
    })


@app.route('/api/dashboard')
def get_dashboard():
    """Obtener datos del dashboard"""
    try:
        data = dashboard.get_summary()
        return jsonify(data)
    except Exception as e:
        logger.error(f'Error obteniendo dashboard: {e}')
        return jsonify({'error': str(e)}), 500


@app.route('/api/threats')
def get_threats():
    """Obtener amenazas detectadas"""
    try:
        threats = threat_detector.get_recent_threats()
        return jsonify(threats)
    except Exception as e:
        logger.error(f'Error obteniendo amenazas: {e}')
        return jsonify({'error': str(e)}), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_event():
    """Analizar evento con IA"""
    try:
        event_data = request.get_json()
        if not event_data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        analysis = ai_analyzer.analyze_security_event(event_data)
        
        # Si es una amenaza crítica, crear alerta
        if analysis.get('severity') in ['high', 'critical']:
            alert_manager.create_alert(analysis)
        
        return jsonify(analysis)
    except Exception as e:
        logger.error(f'Error analizando evento: {e}')
        return jsonify({'error': str(e)}), 500


@app.route('/api/alerts')
def get_alerts():
    """Obtener alertas activas"""
    try:
        alerts = alert_manager.get_active_alerts()
        return jsonify(alerts)
    except Exception as e:
        logger.error(f'Error obteniendo alertas: {e}')
        return jsonify({'error': str(e)}), 500


@app.route('/api/health')
def health_check():
    """Estado del sistema"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'modules': {
            'ai_analyzer': ai_analyzer.is_healthy(),
            'threat_detector': threat_detector.is_healthy(),
            'alert_manager': alert_manager.is_healthy(),
            'siem': siem.is_healthy()
        }
    })


if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    env = os.getenv('FLASK_ENV', 'development')
    
    logger.info(f'🚀 Iniciando CentinelaBot en puerto {port}')
    logger.info(f'📊 Dashboard disponible en http://localhost:{port}')
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=(env == 'development')
    )