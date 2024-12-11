from flask import Flask
import threading
import time
from flask_cors import CORS
from src.mariaDB.query_users import insert_user, user_exists
from src.mariaDB.query_digital_firm import insert_secure_keys
from src.mariaDB.query_certificates import insert_certificate
from src.mariaDB.query_keys import insert_salt_in_db
from src.utils.digitalSign.DigitalSignManager import generate_rsa_keys
from src.utils.MessageManager import MessageManager
from src.utils.HashManager import HashManager
from src.utils.keys.KeyGen import key_from_user
from src.utils.certificate.CertificateManager import CertificateManager
from src.routes.user_routes import users_bp
from src.routes.challenge_routes import challenges_bp

import logging
logging.basicConfig(level=logging.DEBUG)
 
app = Flask(__name__)
CORS(app)

def run_script():
    time.sleep(10) # nos aseguramos que se haya cargado en su totalidad la db
    print("Insert del usuario admin en la base de datos y todas sus credenciales...")
    adminHash = HashManager.create_hash('admin')
    logging.debug('Creating admin user hash...')
    logging.debug('Admin user hash created %s', adminHash)
    adminPasswordHash = HashManager.create_hash('1234')
    logging.debug('Creating admin user password hash...')
    logging.debug('Admin user hash created %s', adminPasswordHash)
    adminHash_direct = '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918'
    adminPasswordHash_direct = '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4'
    
    if adminHash != adminHash_direct or adminPasswordHash != adminPasswordHash_direct:
        logging.debug('Error in the hash generation of the admin, hashed not equal')
    else:
        logging.debug('Hashes are correct, proceeding to insert the admin in the database')
        if not user_exists(adminHash):
            insert_user(adminHash, adminPasswordHash)
        else:
            logging.debug('app.run() --- Admin already exists in the database')

    
    private, public = generate_rsa_keys() # usadas en firma y en certificado
    key,salt = key_from_user(adminHash)
    private_ciphered = MessageManager.cipher_message(private, key)
    insert_secure_keys(adminHash, private_ciphered, public)
    insert_salt_in_db(private_ciphered, salt)
    
    # Generar el certificado para el admin, devuelve el certificado y la clave privada en formato PEM
    certificate_data = CertificateManager.generate_x509_certificate(
        common_name="ADMIN",
        public_key=public.encode(),
        private_key=private.encode()
    )

    # Extraer el certificado y la clave privada en dos variables separadas
    certificate_pem = certificate_data['certificate_pem']
    private_key_pem = certificate_data['private_key_pem']

    # Imprimir los tipos de las variables para verificar
    logging.debug('The admin certificate has been created and signed: %s with type: %s', certificate_pem, type(certificate_pem))  # type should be <bytes>
    logging.debug('The admin private key has been created: %s with type: %s', private_key_pem, type(private_key_pem))  # type should be <bytes>
    
    # insert certificate in database
    ciphered_private_key_pem = MessageManager.cipher_message(private_key_pem.decode(), key)
    insert_salt_in_db(ciphered_private_key_pem, salt)
    insert_certificate(adminHash, ciphered_private_key_pem, certificate_pem)
    logging.debug('--- Everything has been setted up correctly. Start using the app! --- ')

# Inicia el script en un hilo paralelo
thread = threading.Thread(target=run_script)
thread.daemon = True
thread.start()

app.register_blueprint(users_bp)
app.register_blueprint(challenges_bp)

if __name__ == '__main__':
    app.run(debug=True)
