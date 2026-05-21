import token
import requests

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
      url = "https://graph.microsoft.com/v1.0/me/messages?$select=subject,from,receivedDateTime,body&$top=50"
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
                "body": mail.get("body", {}).get("content"),
                "received": mail.get("receivedDateTime")
            })
      return mails
      print(mails)


