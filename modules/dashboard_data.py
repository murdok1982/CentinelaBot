#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Datos del Dashboard
"""

import logging
from datetime import datetime, timedelta
import random

logger = logging.getLogger('CentinelaBot.Dashboard')


class DashboardData:
    """Generador de datos para el dashboard"""
    
    def __init__(self):
        logger.info('✅ Dashboard data inicializado')
    
    def get_summary(self):
        """
        Obtiene resumen de datos para el dashboard
        
        Returns:
            dict: Datos del dashboard
        """
        return {
            'timestamp': datetime.now().isoformat(),
            'system_status': 'operational',
            'statistics': {
                'threats_detected_today': random.randint(5, 25),
                'alerts_active': random.randint(2, 8),
                'events_processed': random.randint(100, 500),
                'security_score': random.randint(75, 95)
            },
            'recent_activity': self._generate_recent_activity(),
            'threat_distribution': {
                'malware': random.randint(20, 40),
                'intrusion': random.randint(10, 30),
                'anomaly': random.randint(15, 35),
                'phishing': random.randint(5, 20),
                'scan': random.randint(10, 25)
            },
            'severity_breakdown': {
                'critical': random.randint(1, 5),
                'high': random.randint(5, 15),
                'medium': random.randint(10, 30),
                'low': random.randint(20, 50)
            }
        }
    
    def _generate_recent_activity(self):
        """Genera actividad reciente de ejemplo"""
        activities = [
            'Análisis de amenaza completado',
            'Alerta crítica generada',
            'Evento correlacionado en SIEM',
            'Escaneo de vulnerabilidades iniciado',
            'Reporte de seguridad generado'
        ]
        
        recent = []
        for i in range(5):
            recent.append({
                'timestamp': (datetime.now() - timedelta(minutes=random.randint(5, 120))).isoformat(),
                'activity': random.choice(activities),
                'status': random.choice(['success', 'warning', 'info'])
            })
        
        return sorted(recent, key=lambda x: x['timestamp'], reverse=True)
    
    def is_healthy(self):
        """Verifica si el módulo está operativo"""
        return True