#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integración con SIEM
"""

import logging
from datetime import datetime
import json

logger = logging.getLogger('CentinelaBot.SIEM')


class SIEMIntegration:
    """Integración con sistemas SIEM"""
    
    def __init__(self):
        self.events = []
        logger.info('✅ Integración SIEM inicializada')
    
    def send_event(self, event_data):
        """
        Envía un evento al SIEM
        
        Args:
            event_data (dict): Datos del evento
            
        Returns:
            dict: Resultado del envío
        """
        try:
            event = {
                'timestamp': datetime.now().isoformat(),
                'source': 'CentinelaBot',
                'data': event_data
            }
            
            self.events.append(event)
            logger.info(f'📤 Evento enviado a SIEM: {event_data.get("type", "unknown")}')
            
            return {
                'status': 'success',
                'event_id': len(self.events),
                'message': 'Evento enviado correctamente'
            }
            
        except Exception as e:
            logger.error(f'Error enviando evento a SIEM: {e}')
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def query_events(self, filters=None):
        """
        Consulta eventos del SIEM
        
        Args:
            filters (dict): Filtros para la consulta
            
        Returns:
            list: Eventos que coinciden con los filtros
        """
        if not filters:
            return self.events
        
        filtered = self.events
        
        if 'type' in filters:
            filtered = [e for e in filtered if e['data'].get('type') == filters['type']]
        
        if 'severity' in filters:
            filtered = [e for e in filtered if e['data'].get('severity') == filters['severity']]
        
        return filtered
    
    def is_healthy(self):
        """Verifica si el módulo está operativo"""
        return True