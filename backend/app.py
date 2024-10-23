from flask import Flask
from flask_cors import CORS
from src.UserManager import users_bp
app = Flask(__name__)
CORS(app)

app.register_blueprint(users_bp)

if __name__ == '__main__':
    app.run(debug=True)
