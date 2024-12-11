""" 
    This module is responsible for managing the creation, deletion, edition and user login.
"""

import logging

from flask import Blueprint, Flask, jsonify, make_response, request
from src.mariaDB.query_certificates import insert_certificate
from src.mariaDB.query_digital_firm import insert_secure_keys
from src.mariaDB.query_keys import get_salt_from_db, insert_salt_in_db
from src.mariaDB.query_users import get_user_password, insert_user
from src.utils.certificate.CertificateManager import CertificateManager
from src.utils.digitalSign.DigitalSignManager import generate_rsa_keys
from src.utils.HashManager import HashManager
from src.utils.keys import KeyGen
from src.utils.MessageManager import MessageManager

logging.basicConfig(level=logging.DEBUG)
from src.mariaDB.query_certificates import get_certificates

users_bp = Blueprint("users", __name__)


@users_bp.route("/hello", methods=["GET"])
def hello():
    response = make_response(jsonify({"response": "hello!"}), 200)
    return response


@users_bp.route("/create_user", methods=["POST"])
def create_user():
    """
    Create a new user in the database:
    1. Get user name and password
    2. Hash the user and password
    3. Check that the user does not exist
    4. Insert the user and password in the database -> Use insert_user()
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Hash the user and password before inserting them in the database
    hashed_user = HashManager.create_hash(username)
    hashed_password = HashManager.create_hash(password)

    hashed_admin = HashManager.create_hash("admin")

    # NOTE: Esta función(insert_user) podría no ser un bool sino devolver un response para tener propagación de errores
    if insert_user(hashed_user, hashed_password):
        # Generate the digital sign keys
        private_key, public_key = generate_rsa_keys()
        logging.debug(
            "Digital Sign keys generated: public key: %s  \n--- private key: %s",
            public_key,
            private_key,
        )
        logging.debug(
            "Digital sign keys types: public key type: %s --- private key type: %s",
            type(public_key),
            type(private_key),
        )

        # Generate the key and salt for the user
        key, salt = KeyGen.key_from_user(hashed_user, 256)
        # Cipher the private key of the user
        private_key_ciphered = MessageManager.cipher_message(private_key, key)
        # Insert the salt in the database for the user
        insert_salt_in_db(private_key_ciphered, salt)
        logging.debug(
            "Digital Sign private ciphered key: %s",
            private_key_ciphered,
        )
        logging.debug(
            "type of private key: %s",
            type(private_key_ciphered),
        )

        if not insert_secure_keys(hashed_user, private_key_ciphered, public_key):
            response = make_response(
                jsonify({"response": "Ups, something went wrong"}), 422
            )
            return response

        # Generate the certificate for the user
        private_emisor_private_key = get_certificates(hashed_admin)[2]
        # Decipher the private key of the admin
        admin_salt = get_salt_from_db(private_emisor_private_key)
        admin_key, admin_salt = KeyGen.key_from_user(hashed_admin, salt=admin_salt)
        emisor_private_key = MessageManager.decipher_message(
            private_emisor_private_key, admin_key
        )
        # Create the certificate for the user
        certificate_data = (
            CertificateManager.generate_x509_certificate_for_another_entity(
                issuer_private_key=emisor_private_key.encode(),
                issuer_name="ADMIN",
                subject_name=hashed_user,
                subject_public_key=public_key.encode(),
            )
        )

        # Extraer el certificado y la clave privada en dos variables separadas
        certificate_pem = certificate_data["certificate_pem"]

        # Imprimir los tipos de las variables para verificar
        logging.debug(
            "The admin certificate has been created and signed: %s with type: %s",
            certificate_pem,
            type(certificate_pem),
        )  # type should be <bytes>

        # insert certificate in database: private_emisor_private_key
        if not insert_certificate(
            hashed_user, private_emisor_private_key, certificate_pem
        ):
            response = make_response(
                jsonify({"response": "Ups, something went wrong"}), 422
            )
            return response

    else:
        # En el caso de que el hash ya exista, devolvemos un error
        response = make_response(jsonify({"response": "Username already exists"}), 422)
    response = make_response(jsonify({"response": "User was created!"}), 201)
    return response


@users_bp.route("/login_user", methods=["POST"])
def login_user():
    """
    Login a user:
    1. Get user name and password
    2. Hash the user
    3. Get the user password from the database
    4. Check that the hash is correct -> Use hash_manager.verify_hash()
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Hash the user and password before inserting them in the database
    hashed_user = HashManager.create_hash(username)

    hashed_password = get_user_password(hashed_user)

    # The get_user_password method should return the hashed password of the user.
    # If the password is correct, the user exists and can log in.
    if HashManager.verify_hash(password, hashed_password):
        response = make_response(jsonify({"response": "User exists!"}), 201)
    else:
        response = make_response(
            jsonify({"response": "Username or password is incorrect"}), 422
        )
    return response
