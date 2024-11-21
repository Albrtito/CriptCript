""" 
    This module is responsible for managing the creation, deletion, edition and user login.
"""

from flask import Flask, jsonify, make_response, request
from src.mariaDB.query_users import insert_user, get_user_password
from src.utils.HashManager import HashManager
from src.utils.digitalSign.DigitalSignManager import generate_rsa_keys
from src.utils.keys import KeyGen
from src.utils.MessageManager import MessageManager
from flask import Blueprint
import logging
logging.basicConfig(level=logging.DEBUG)

users_bp = Blueprint('users', __name__)

@users_bp.route('/hello', methods=['GET'])
def hello():
    response = make_response(
            jsonify({"response": "hello!"}), 200
        )
    return(response)

@users_bp.route('/create_user', methods=['POST'])
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

    # NOTE: Esta función(insert_user) podría no ser un bool sino devolver un response para tener propagación de errores
    if insert_user(hashed_user, hashed_password):
        private_key, public_key = generate_rsa_keys()
        logging.debug('Digital Sign keys generated: public key: %s --- private key: %s', public_key, private_key)
        logging.debug('Digital sign keys types: public key type: %s --- private key type: %s', type(public_key), type(private_key))
        key = KeyGen.key_from_user(hashed_user, 256)
        private_key_ciphered = MessageManager.cipher_message(private_key, key)
        logging.debug('Digital Sign private ciphered key: %s', private_key_ciphered)
        
        private_key_deciphered = MessageManager.decipher_message(private_key_ciphered, key)
        logging.debug('Digital Sign private deciphered key: %s', private_key_deciphered)

        # En el caso de que el hash no exista devolvemos un mensaje de éxito
        response = make_response(
            jsonify({"response": "User created successfully!"}), 201
        )
    else:
        # En el caso de que el hash ya exista, devolvemos un error
        response = make_response(jsonify({"response": "Username already exists"}), 422)

    return response

@users_bp.route('/login_user', methods=['POST'])
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
        response = make_response(jsonify({"response": "Username or password is incorrect"}), 422)
    return response
