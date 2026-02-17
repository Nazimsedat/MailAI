import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

class GeminiService:
    def __init__(self):
        load_dotenv()
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel("gemini-3-flash-preview")

    def ask_about_mail(self, mail_content: str,user_prompt:str)-> str:
        promt = f"""
        Aşağıdaki e-postayı referans alarak kullanıcı sorusunu cevapla.

        E-posta:
        {mail_content}
        Kullanıcı Sorusu:
        {user_prompt}
        """
        response = self.model.generate_content(promt)
        return response.text
    
    def today_all_mails(self,mails_all:str)->str:
        promt = f"""
        Bugün gelen maillerden önemli olanları seç ve bana özetle. Markdown eklemeden, yaptığın özeti HTML formatında ver. akış şablonu olarak BAŞLIK:
...

ÖZET:
...

ÖNEMLİ NOKTALAR:
- ...
- ...
- ... bu şablonu kullan.Başlıkları kalın yaz. Maillerin içeriği aşağıda verilmiştir:
        {mails_all}
        """
        response = self.model.generate_content(promt)
        return response.text