from flask import Flask
import threading
import time
from flask_cors import CORS
from src.mariaDB.query_users import insert_user
from src.mariaDB.query_digital_firm import insert_secure_keys
from src.utils.digitalSign.DigitalSignManager import generate_rsa_keys
from src.utils.MessageManager import MessageManager
from src.utils.keys.KeyGen import key_from_user
from src.routes.user_routes import users_bp
from src.routes.challenge_routes import challenges_bp
app = Flask(__name__)
CORS(app)

def run_script():
    time.sleep(10)
    print("Insert del usuario admin en la base de datos y todas sus credenciales...")
    adminHash = '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918'
    adminPasswordHash = '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4'
    insert_user( adminHash, adminPasswordHash)
    private, public = generate_rsa_keys()
    key = key_from_user(adminHash)
    private_ciphered = MessageManager.cipher_message(private, key)
    insert_secure_keys(adminHash, private_ciphered, public)

# Inicia el script en un hilo paralelo
thread = threading.Thread(target=run_script)
thread.daemon = True
thread.start()

app.register_blueprint(users_bp)
app.register_blueprint(challenges_bp)

if __name__ == '__main__':
    app.run(debug=True)
