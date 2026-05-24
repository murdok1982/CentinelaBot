import json
import logging
import urllib.request
from openai import OpenAI
from config import Config

logger = logging.getLogger("centinela.ai")


class AIAnalyzer:
    def __init__(self):
        self.provider = Config.AI_PROVIDER
        self.openai_client = None
        self.ollama_available = False

        if Config.OPENAI_API_KEY:
            self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
            logger.info("OpenAI client initialized")
        else:
            logger.info("No OpenAI API key configured")

        try:
            req = urllib.request.Request(
                f"{Config.OLLAMA_BASE_URL}/api/tags",
                method="GET"
            )
            urllib.request.urlopen(req, timeout=3)
            self.ollama_available = True
            logger.info("Ollama available at %s", Config.OLLAMA_BASE_URL)
        except Exception:
            logger.warning("Ollama not available at %s", Config.OLLAMA_BASE_URL)

    def _call_ollama(self, prompt, system):
        import json as j
        data = j.dumps({
            "model": Config.OLLAMA_MODEL,
            "prompt": f"[INST] <<SYS>>\n{system}\n<</SYS>>\n\n{prompt} [/INST]",
            "stream": False,
            "options": {"temperature": 0.3, "num_predict": 512}
        }).encode()
        req = urllib.request.Request(
            f"{Config.OLLAMA_BASE_URL}/api/generate",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        resp = urllib.request.urlopen(req, timeout=30)
        result = j.loads(resp.read())
        return result.get("response", "")

    def _call_openai(self, prompt, system):
        resp = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        return resp.choices[0].message.content

    def analyze_security_event(self, event_data):
        system = (
            "Eres un analista de ciberseguridad experto. "
            "Analiza eventos de seguridad y responde SOLO con JSON "
            "con campos: severity (low/medium/high/critical), analysis, recommendations."
        )
        prompt = (
            f"Tipo: {event_data.get('event_type', 'unknown')}\n"
            f"Origen: {event_data.get('source', 'unknown')}\n"
            f"Descripcion: {event_data.get('description', '')}\n"
            f"Detalles: {event_data.get('details', {})}"
        )

        try:
            if self.provider == "openai" and self.openai_client:
                text = self._call_openai(prompt, system)
            elif self.provider == "ollama" and self.ollama_available:
                text = self._call_ollama(prompt, system)
            else:
                return self._fallback(event_data)

            try:
                result = json.loads(text)
            except json.JSONDecodeError:
                result = {"severity": "medium", "analysis": text, "recommendations": "Revisar manualmente"}

            result["ai_powered"] = True
            result["provider"] = self.provider
            return result

        except Exception as e:
            logger.error("AI analysis error: %s", e)
            return self._fallback(event_data)

    def _fallback(self, event_data):
        et = event_data.get("event_type", "unknown")
        severity_map = {"malware": "high", "intrusion": "critical", "anomaly": "medium", "scan": "low"}
        return {
            "severity": severity_map.get(et, "medium"),
            "analysis": f"Evento {et} detectado. Analisis basico sin IA.",
            "recommendations": "Revisar logs manualmente.",
            "ai_powered": False,
            "provider": "fallback"
        }

    def is_healthy(self):
        return True
