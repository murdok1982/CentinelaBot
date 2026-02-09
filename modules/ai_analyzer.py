#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analizador de Seguridad con IA
"""

import os
import logging
from datetime import datetime
from openai import OpenAI

logger = logging.getLogger('CentinelaBot.AI')


class AIAnalyzer:
    """Analizador de eventos de seguridad usando IA"""
    
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        self.client = OpenAI(api_key=api_key) if api_key else None
        self.enabled = api_key is not None
        
        if not self.enabled:
            logger.warning('⚠️ OpenAI API key no configurada. Análisis IA deshabilitado.')
        else:
            logger.info('✅ Analizador IA inicializado')
    
    def analyze_security_event(self, event_data):
        """
        Analiza un evento de seguridad con IA
        
        Args:
            event_data (dict): Datos del evento a analizar
            
        Returns:
            dict: Análisis del evento con severidad y recomendaciones
        """
        if not self.enabled:
            return self._fallback_analysis(event_data)
        
        try:
            prompt = self._build_prompt(event_data)
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un experto analista de ciberseguridad. Analiza eventos de seguridad y proporciona evaluaciones detalladas con severidad (low, medium, high, critical) y recomendaciones."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            analysis_text = response.choices[0].message.content
            
            return {
                'event_id': event_data.get('id', 'unknown'),
                'timestamp': datetime.now().isoformat(),
                'analysis': analysis_text,
                'severity': self._extract_severity(analysis_text),
                'ai_powered': True
            }
            
        except Exception as e:
            logger.error(f'Error en análisis IA: {e}')
            return self._fallback_analysis(event_data)
    
    def _build_prompt(self, event_data):
        """Construye el prompt para el análisis"""
        return f"""Analiza el siguiente evento de seguridad:

Tipo: {event_data.get('type', 'unknown')}
Origen: {event_data.get('source', 'unknown')}
Descripción: {event_data.get('description', 'Sin descripción')}
Datos adicionales: {event_data.get('details', {})}

Proporciona:
1. Severidad (low/medium/high/critical)
2. Análisis de la amenaza
3. Recomendaciones de respuesta
"""
    
    def _extract_severity(self, text):
        """Extrae el nivel de severidad del análisis"""
        text_lower = text.lower()
        if 'critical' in text_lower:
            return 'critical'
        elif 'high' in text_lower:
            return 'high'
        elif 'medium' in text_lower:
            return 'medium'
        else:
            return 'low'
    
    def _fallback_analysis(self, event_data):
        """Análisis básico cuando IA no está disponible"""
        severity_map = {
            'malware': 'high',
            'intrusion': 'critical',
            'anomaly': 'medium',
            'scan': 'low'
        }
        
        event_type = event_data.get('type', 'unknown')
        severity = severity_map.get(event_type, 'medium')
        
        return {
            'event_id': event_data.get('id', 'unknown'),
            'timestamp': datetime.now().isoformat(),
            'analysis': f'Evento de tipo {event_type} detectado. Análisis básico sin IA.',
            'severity': severity,
            'ai_powered': False
        }
    
    def is_healthy(self):
        """Verifica si el módulo está operativo"""
        return True