#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestor de Alertas
"""

import logging
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

logger = logging.getLogger('CentinelaBot.AlertManager')


class AlertManager:
    """Gestor de alertas de seguridad"""
    
    def __init__(self):
        self.alerts = []
        self.email_enabled = self._check_email_config()
        logger.info('✅ Gestor de alertas inicializado')
        self._generate_sample_alerts()
    
    def _check_email_config(self):
        """Verifica si la configuración de email está disponible"""
        required = ['SMTP_SERVER', 'SMTP_PORT', 'SMTP_USER', 'SMTP_PASSWORD']
        configured = all(os.getenv(key) for key in required)
        
        if not configured:
            logger.warning('⚠️ Configuración de email incompleta. Notificaciones por email deshabilitadas.')
        
        return configured
    
    def _generate_sample_alerts(self):
        """Genera alertas de ejemplo"""
        sample_alerts = [
            {
                'id': 'ALT-001',
                'timestamp': datetime.now().isoformat(),
                'severity': 'high',
                'title': 'Acceso no autorizado detectado',
                'description': 'Se detectó un intento de acceso no autorizado desde IP sospechosa',
                'status': 'active'
            },
            {
                'id': 'ALT-002',
                'timestamp': datetime.now().isoformat(),
                'severity': 'medium',
                'title': 'Anomalía en tráfico de red',
                'description': 'Tráfico de red inusual detectado en el segmento 192.168.1.0/24',
                'status': 'investigating'
            }
        ]
        self.alerts.extend(sample_alerts)
    
    def create_alert(self, analysis):
        """Crea una nueva alerta"""
        alert = {
            'id': f'ALT-{len(self.alerts) + 1:03d}',
            'timestamp': datetime.now().isoformat(),
            'severity': analysis.get('severity', 'medium'),
            'title': f"Amenaza {analysis.get('severity', 'medium').upper()} detectada",
            'description': analysis.get('analysis', 'Sin descripción'),
            'status': 'active',
            'event_id': analysis.get('event_id')
        }
        
        self.alerts.append(alert)
        logger.warning(f'🚨 Nueva alerta creada: {alert["id"]} - {alert["title"]}')
        
        # Enviar notificación por email si está configurado
        if self.email_enabled and alert['severity'] in ['high', 'critical']:
            self._send_email_alert(alert)
        
        return alert
    
    def get_active_alerts(self):
        """Obtiene las alertas activas"""
        active = [a for a in self.alerts if a['status'] == 'active']
        return {
            'total': len(active),
            'alerts': sorted(active, key=lambda x: x['timestamp'], reverse=True)
        }
    
    def _send_email_alert(self, alert):
        """Envía notificación por email"""
        try:
            msg = MIMEMultipart()
            msg['From'] = os.getenv('SMTP_USER')
            msg['To'] = os.getenv('ALERT_EMAIL')
            msg['Subject'] = f"🚨 CentinelaBot Alert: {alert['title']}"
            
            body = f"""
            Alerta de Seguridad - CentinelaBot
            
            ID: {alert['id']}
            Severidad: {alert['severity'].upper()}
            Fecha: {alert['timestamp']}
            
            {alert['description']}
            
            --
            CentinelaBot - Sistema de Gestión de Ciberseguridad
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(os.getenv('SMTP_SERVER'), int(os.getenv('SMTP_PORT')))
            server.starttls()
            server.login(os.getenv('SMTP_USER'), os.getenv('SMTP_PASSWORD'))
            server.send_message(msg)
            server.quit()
            
            logger.info(f'✉️ Email de alerta enviado: {alert["id"]}')
            
        except Exception as e:
            logger.error(f'Error enviando email: {e}')
    
    def is_healthy(self):
        """Verifica si el módulo está operativo"""
        return True