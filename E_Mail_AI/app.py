import os
import requests
from flask import Flask, redirect, session, url_for, jsonify,request , render_template
from dotenv import load_dotenv
import msal
from datetime import date, time
from bs4 import BeautifulSoup

load_dotenv()

CLIENT_ID = os.getenv("APP_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")
REDIRECT_URI = os.getenv("REDIRECT_URI")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["User.Read", "Mail.Read"]

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

msal_app = msal.ConfidentialClientApplication(
    CLIENT_ID,
    authority=AUTHORITY,
    client_credential=CLIENT_SECRET
)

@app.route("/")
def index():
    auth_url = msal_app.get_authorization_request_url(
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
        prompt="select_account" 
    )
    return redirect(auth_url)


@app.route("/callback")
def callback():
    if "code" not in session and "code" not in os.environ:
        code = dict(request.args).get("code")
    else:
        code = session.get("code")

    if not code:
        return "Authorization code bulunamadı", 400

    result = msal_app.acquire_token_by_authorization_code(
        code=code,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )

    if "access_token" not in result:
        return jsonify(result), 400

    session["access_token"] = result["access_token"]
    return redirect(url_for("mails"))




@app.route("/mails")
def mails():
    today = date.today()
    token = session.get("access_token")
    if not token:
        return redirect(url_for("index"))

    headers = {
        "Authorization": f"Bearer {token}"
    }

    url = f"https://graph.microsoft.com/v1.0/me/messages?$filter=receivedDateTime ge {today}"

    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        return jsonify({
            "status": r.status_code,
            "error": r.json()
        })

    messages = []
    for mail in r.json().get("value", []):
        messages.append({
            "from": mail["from"]["emailAddress"]["address"],
            "subject": mail["subject"],
            "body": mail["bodyPreview"],
            "received": mail["receivedDateTime"]
        })

    return render_template("mails.html",messages=messages)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://login.microsoftonline.com/common/oauth2/v2.0/logout"
        "?post_logout_redirect_uri=http://localhost:5000/"
    )


@app.route("/Home")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)