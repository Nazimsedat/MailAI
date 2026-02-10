import requests

def get_all_mails(token):
      headers = {
        "Authorization": f"Bearer {token}"        
    }
      
      url = "https://graph.microsoft.com/v1.0/me/messages?$top=50"
      mails = []

      while url:
            r = requests.get(url,headers=headers)
            r.raise_for_status()
            data = r.json()

            for mail in data.get("value",[]):
                  mails.append({
                    "from": mail["from"]["emailAddress"]["address"],
                    "subject": mail["subject"],
                    "body": mail["bodyPreview"],
                    "received": mail["receivedDateTime"]
                  })
            urtlink = data.get("@odata.nextlink")

            return mails

