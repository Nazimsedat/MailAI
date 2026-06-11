import token
import requests
import json
from bs4 import BeautifulSoup

def get_all_mails(token):
      headers = {
        "Authorization": f"Bearer {token}"        
    }
      
      url = "https://graph.microsoft.com/v1.0/me/messages?$top=100"
      mails = []
    
      while url:
            r = requests.get(url,headers=headers)
            r.raise_for_status()
            data = r.json()

            for mail in data.get("value",[]):
                  mails.append({
                    "id": mail.get("id"),
                    "from": mail.get("from", {}).get("emailAddress", {}).get("address"),
                    "subject": mail.get("subject"),
                    "body": mail.get("bodyPreview"),
                    "received": mail.get("receivedDateTime")
                  })
            url = data.get("@odata.nextlink")

            return mails


def AI_Prompt_mail(token):
      url = "https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages?$select=subject,from,receivedDateTime,bodyPreview&$top=50"
  
      headers = {
        "Authorization": f"Bearer {token}"
      }
      response = requests.get(url, headers=headers)
      response.raise_for_status()

      data = response.json()
      mails = []

      for mail in data.get("value", []):
            mails.append({
                "from": mail.get("from", {}).get("emailAddress", {}).get("address"),
                "subject": mail.get("subject"),
                "body": mail.get("bodyPreview"),
                "received": mail.get("receivedDateTime")
            })

      cleanMail = []

      for mail in mails:
            soup = BeautifulSoup(mail["body"], "html.parser")

            for tag in soup(["script", "style","img"]):
                  tag.decompose()
            
            text = soup.get_text(" ", strip=True)

            cleanMail.append({
                  "from": mail["from"],
                  "subject": mail["subject"],
                  "body": text,
                  "received": mail["received"]
            })

            print(json.dumps(cleanMail, indent=4, ensure_ascii=False))
      return cleanMail
           