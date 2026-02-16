import os
from dotenv import load_dotenv
from flask import Blueprint,redirect,request,session,url_for,jsonify
from auth import msal_client
import config


auth_bp = Blueprint("auth",__name__)
msal_app = msal_client.get_msal_app()

SCOPES = ["User.Read","Mail.Read"]
REDIRECT_URI = os.getenv("REDIRECT_URI")


@auth_bp.route("/loginmicrosoft")
def index():
    auth_url = msal_app.get_authorization_request_url(
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
        prompt="select_account"
    )
    return redirect(auth_url)


@auth_bp.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Auth Kodu yok", 400
    
    result = msal_app.acquire_token_by_authorization_code(
        code=code,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    if "access_token" not in result:
        return jsonify(result),400
    
    session["access_token"] = result["access_token"]
    return redirect(url_for("mail.mails"))

    