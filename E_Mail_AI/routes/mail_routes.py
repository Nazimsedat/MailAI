import base64
from io import BytesIO
from flask import Blueprint, send_file, session, redirect, url_for, render_template
from services.mail_service import get_all_mails,AI_Prompt_mail
from services.AI_service import GeminiService
import requests

mail_bp = Blueprint("mail",__name__)
gemini_service = GeminiService()
@mail_bp.route("/")
def index():
    return render_template("index.html")

@mail_bp.route("/mails")
def mails():
    token = session.get("access_token")
    if not token:
        return redirect(url_for("auth.index"))
    
    messages = get_all_mails(token)
    ai_prompt_mails = AI_Prompt_mail(token)
    print(ai_prompt_mails)
    AI_prompt = gemini_service.today_all_mails(ai_prompt_mails)
    print(AI_prompt)
    return render_template("mails.html",messages=messages,ai_prompt_mails=ai_prompt_mails,AI_prompt=AI_prompt)

@mail_bp.route("/mail/<string:mail_id>")
def mail_detail(mail_id):
    access_token = session.get("access_token")

    if not access_token:
        return redirect(url_for("auth.index"))

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    url = f"https://graph.microsoft.com/v1.0/me/messages/{mail_id}?$select=subject,from,receivedDateTime,body&$expand=attachments"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return "Mail alınamadı", 500

    mail = response.json()

    return render_template("mail_detail.html", mail=mail)

@mail_bp.route("/mail/<mail_id>/attachment/<attachment_id>",methods=["POST"])
def download_attachment(mail_id, att_id):
    token = session.get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    
    url = f"https://graph.microsoft.com/v1.0/me/messages/{mail_id}/attachments/{att_id}"
    resp = requests.get(url, headers=headers)
    att = resp.json()

    file_data = base64.b64decode(att["contentBytes"])
    return f"Attachment {att} downloaded from mail {mail_id}"