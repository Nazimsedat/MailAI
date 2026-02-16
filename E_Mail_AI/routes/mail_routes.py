from flask import Blueprint, session, redirect, url_for, render_template
from services.mail_service import get_all_mails

mail_bp = Blueprint("mail",__name__)

@mail_bp.route("/")
def index():
    return render_template("index.html")

@mail_bp.route("/mails")
def mails():
    token = session.get("access_token")
    if not token:
        return redirect(url_for("auth.index"))
    
    messages = get_all_mails(token)
    return render_template("mails.html",messages=messages)