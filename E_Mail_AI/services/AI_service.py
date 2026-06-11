import os

import requests
from dotenv import load_dotenv

load_dotenv()

class SisAIService:
    def __init__(self):
        self.url = os.getenv("SISAI_URL", "http://192.168.2.154:11434/api/generate")
        self.model = os.getenv("SISAI_MODEL", "qwen2.5:latest")

    def _generate(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.2,
            },
        }
        response = requests.post(self.url, json=payload, timeout=120)
        if response.status_code == 404:
            raise RuntimeError(f"SisAI modeli bulunamadi: {self.model}")
        response.raise_for_status()
        data = response.json()
        return data.get("response") or data.get("text") or ""

  

    def ask_about_mails(self, mails_all: str, user_prompt: str) -> str:
        prompt = f"{mails_all}\n\n{user_prompt}"
        return self._generate(prompt)

