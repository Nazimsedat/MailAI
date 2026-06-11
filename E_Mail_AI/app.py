from uuid import uuid4

from flask import Flask, session
from config import FLASK_SECRET_KEY
from routes.auth_routes import auth_bp
from routes.mail_routes import mail_bp

app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY
app.config["SESSION_BOOT_ID"] = uuid4().hex

VOLATILE_SESSION_KEYS = (
    "mails_summary",
    "mails_chat_history",
    "chat_history",
)


@app.before_request
def reset_chat_session_after_restart():
    boot_id = app.config["SESSION_BOOT_ID"]
    if session.get("_boot_id") == boot_id:
        return

    for key in VOLATILE_SESSION_KEYS:
        session.pop(key, None)

    session["_boot_id"] = boot_id
    session.modified = True

app.register_blueprint(auth_bp)
app.register_blueprint(mail_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

