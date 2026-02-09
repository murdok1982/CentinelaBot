#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Detector de Amenazas
"""

import logging
from datetime import datetime, timedelta
import random

logger = logging.getLogger('CentinelaBot.ThreatDetector')


class ThreatDetector:
    """Detector de amenazas de seguridad"""
    
    def __init__(self):
        self.threats = []
        logger.info('✅ Detector de amenazas inicializado')
        self._generate_sample_threats()
    
    def _generate_sample_threats(self):
        """Genera amenazas de ejemplo para demostración"""
        threat_types = [
            {'type': 'malware', 'severity': 'high', 'description': 'Posible malware detectado en endpoint'},
            {'type': 'intrusion', 'severity': 'critical', 'description': 'Intento de acceso no autorizado detectado'},
            {'type': 'anomaly', 'severity': 'medium', 'description': 'Comportamiento anómalo en tráfico de red'},
            {'type': 'scan', 'severity': 'low', 'description': 'Escaneo de puertos detectado'},
            {'type': 'phishing', 'severity': 'high', 'description': 'Email de phishing detectado'}
        ]
        
        for i, threat_template in enumerate(threat_types):
            threat = {
                'id': f'THR-{1000 + i}',
                'timestamp': (datetime.now() - timedelta(hours=random.randint(1, 24))).isoformat(),
                'type': threat_template['type'],
                'severity': threat_template['severity'],
                'description': threat_template['description'],
                'source': f'192.168.1.{random.randint(10, 254)}',
                'status': random.choice(['active', 'investigating', 'resolved'])
            }
            self.threats.append(threat)
    
    def get_recent_threats(self, limit=20):
        """Obtiene las amenazas recientes"""
        return {
            'total': len(self.threats),
            'threats': sorted(self.threats, key=lambda x: x['timestamp'], reverse=True)[:limit]
        }
    
    def detect_threat(self, event_data):
        """Detecta si un evento es una amenaza"""
        # Implementación básica de detección
        suspicious_patterns = ['malware', 'intrusion', 'attack', 'breach', 'exploit']
        
        event_text = str(event_data).lower()
        for pattern in suspicious_patterns:
            if pattern in event_text:
                threat = {
                    'id': f'THR-{len(self.threats) + 1000}',
                    'timestamp': datetime.now().isoformat(),
                    'type': pattern,
                    'severity': 'high',
                    'description': f'{pattern.capitalize()} detectado',
                    'source': event_data.get('source', 'unknown'),
                    'status': 'active'
                }
                self.threats.append(threat)
                return threat
        
        return None
    
    def is_healthy(self):
        """Verifica si el módulo está operativo"""
        return True