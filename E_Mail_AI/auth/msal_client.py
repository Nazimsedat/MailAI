import os
from dotenv import load_dotenv
import msal


load_dotenv()
CLIENT_ID = os.getenv("APP_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")
AUTHORTY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["User.Read","Mail.Read"]
FLASK_SECRET = os.getenv("FLASK_SECRET_KEY")

def get_msal_app():
    return msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORTY,
        client_credential=CLIENT_SECRET
    )