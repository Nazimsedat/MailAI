import os

import requests
from dotenv import load_dotenv

load_dotenv()


class GeminiService:
    def __init__(self):
        load_dotenv()
        import google.generativeai as genai

        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel("gemini-3-flash-preview")

    def ask_about_mail(self, mail_content: str, user_prompt: str) -> str:
        prompt = f"""
        Asagidaki e-postayi referans alarak kullanici sorusunu cevapla.

        E-posta:
        {mail_content}
        Kullanici Sorusu:
        {user_prompt}
        """
        response = self.model.generate_content(prompt)
        return response.text

    def ask_about_mails(self, mails_all: str, user_prompt: str) -> str:
        prompt = f"""
        Asagidaki gelen e-postalari referans alarak kullanicinin sorusunu cevapla.
        Cevabini kisa, net ve Turkce ver. Bir mailden bahsediyorsan gondereni ve konuyu belirt.

        Gelen e-postalar:
        {mails_all}

        Kullanici Sorusu:
        {user_prompt}
        """
        response = self.model.generate_content(prompt)
        return response.text

    def today_all_mails(self, mails_all: str) -> str:
        prompt = f"""
        Bugun gelen maillerden onemli olanlari sec ve bana ozetle.
        Markdown eklemeden, yaptigin ozeti HTML formatinda ver.
        Akis sablonu olarak su yapidakini kullan:

        BASLIK:
        ...

        OZET:
        ...

        ONEMLI NOKTALAR:
        - ...
        - ...
        - ...

        Basliklari kalin yaz. Maillerin icerigi asagida verilmistir:
        {mails_all}
        """
        response = self.model.generate_content(prompt)
        return response.text


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

    def ask_about_mail(self, mail_content: str, user_prompt: str) -> str:
        prompt = f"""
        Sen Turkce konusan bir e-posta asistanisin.
        Sadece Turkce cevap ver. Ingilizce kelime kullanma.
        Cevabin kisa, net ve anlasilir olsun.
        Asagidaki e-postayi referans alarak kullanici sorusunu cevapla.

        E-posta:
        {mail_content}
        Kullanici Sorusu:
        {user_prompt}
        """
        return self._generate(prompt)

    def ask_about_mails(self, mails_all: str, user_prompt: str) -> str:
        prompt = f"""
        Sen Turkce konusan bir e-posta asistanisin.
        Sadece Turkce cevap ver. Ingilizce kelime kullanma.
        Cevabin kisa, net ve anlasilir olsun.
        Asagidaki gelen e-postalari referans alarak kullanicinin sorusunu cevapla.
        Cevabini kisa, net ve Turkce ver. Bir mailden bahsediyorsan gondereni ve konuyu belirt.

        Gelen e-postalar:
        {mails_all}

        Kullanici Sorusu:
        {user_prompt}
        """
        return self._generate(prompt)

    def today_all_mails(self, mails_all: str) -> str:
        prompt = f"""
        Sen Turkce konusan bir e-posta asistanisin.
        Sadece Turkce cevap ver. Ingilizce kelime kullanma.
        Bugun gelen maillerden onemli olanlari sec ve bana ozetle.
        Markdown eklemeden, yaptigin ozeti HTML formatinda ver.
        Akis sablonu olarak su yapidakini kullan:

        BASLIK:
        ...

        OZET:
        ...

        ONEMLI NOKTALAR:
        - ...
        - ...
        - ...

        Basliklari kalin yaz. Maillerin icerigi asagida verilmistir:
        {mails_all}
        """
        return self._generate(prompt)
