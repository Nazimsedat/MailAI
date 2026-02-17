from flask import Flask
from config import FLASK_SECRET_KEY
from routes.auth_routes import auth_bp
from routes.mail_routes import mail_bp

app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY

app.register_blueprint(auth_bp)
app.register_blueprint(mail_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

