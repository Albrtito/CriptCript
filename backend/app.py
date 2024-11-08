from flask import Flask
from flask_cors import CORS
from src.routes.user_routes import users_bp
from src.routes.challenge_routes import challenges_bp
app = Flask(__name__)
CORS(app)

app.register_blueprint(users_bp)
app.register_blueprint(challenges_bp)

if __name__ == '__main__':
    app.run(debug=True)
