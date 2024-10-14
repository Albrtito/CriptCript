from flask import Flask
from users import users_bp

app = Flask(__name__)

app.register_blueprint(users_bp)