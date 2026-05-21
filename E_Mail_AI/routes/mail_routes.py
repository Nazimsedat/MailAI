import base64
from io import BytesIO
from flask import Blueprint, send_file, session, redirect, url_for, render_template
from services.mail_service import get_all_mails,AI_Prompt_mail
from services.AI_service import SisAIService
import requests
from flask import request
import json
from bs4 import BeautifulSoup

mail_bp = Blueprint("mail",__name__)
ai_service = SisAIService()

@mail_bp.route("/")
def index():
    return render_template("index.html")


@mail_bp.route("/mails",methods=["GET","POST"])
def mails():
    token = session.get("access_token")
    if not token:
        return redirect(url_for("auth.index"))
    AI_prompt = session.get("mails_summary")
    messages = get_all_mails(token)
    ai_prompt_mails = AI_Prompt_mail(token)

    if "mails_chat_history" not in session:
        session["mails_chat_history"] = []

    if request.method == "POST":
        action = request.form.get("action")

        if action == "summary":
            AI_prompt = ai_service.today_all_mails(ai_prompt_mails)
            session["mails_summary"] = AI_prompt
            session.modified = True

        if action == "mails_chat":
            user_message = request.form.get("user_message")

            if user_message:
                session["mails_chat_history"].append({
                    "role": "user",
                    "content": user_message
                })

                ai_response = ai_service.ask_about_mails(ai_prompt_mails, user_message)

                session["mails_chat_history"].append({
                    "role": "ai",
                    "content": ai_response
                })

                session.modified = True
        
    return render_template(
        "mails.html",
        messages=messages,
        ai_prompt_mails=ai_prompt_mails,
        AI_prompt=AI_prompt,
        mails_chat_history=session.get("mails_chat_history", [])
    )


@mail_bp.route("/mail/<string:mail_id>", methods=["POST", "GET"])
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

    # HTML temizleme
    soup = BeautifulSoup(mail["body"]["content"], "html.parser")
    clean_body = soup.get_text()

    # Chat history yoksa oluştur
    if "chat_history" not in session:
        session["chat_history"] = []

    if request.method == "POST" and request.form.get("action") == "ai_chat":

        user_message = request.form.get("user_message")

        if user_message:

            # Kullanıcı mesajını ekle
            session["chat_history"].append({
                "role": "user",
                "content": user_message
            })

            # AI prompt oluştur
            full_prompt = f"""
            Mail İçeriği:
            {clean_body}

            Kullanıcı Sorusu:
            {user_message}
            """

            ai_response = ai_service.ask_about_mail(clean_body,user_message)

            # AI cevabını ekle
            session["chat_history"].append({
                "role": "ai",
                "content": ai_response
            })

            session.modified = True

    return render_template(
        "mail_detail.html",
        mail=mail,
        chat_history=session.get("chat_history", [])
    )

@mail_bp.route("/mail/<mail_id>/attachment/<attachment_id>",methods=["POST"])
def download_attachment(mail_id, att_id):
    token = session.get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    
    url = f"https://graph.microsoft.com/v1.0/me/messages/{mail_id}/attachments/{att_id}"
    resp = requests.get(url, headers=headers)
    att = resp.json()

    file_data = base64.b64decode(att["contentBytes"])
    return f"Attachment {att} downloaded from mail {mail_id}"
