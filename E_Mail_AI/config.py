import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("APP_ID")
TENANT_ID = os.getenv("TENANT_ID")
REDIRECT_URI = os.getenv("REDIRECT_URI")

AUTHORTY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["User.Read","Mail,Readd"]

FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")