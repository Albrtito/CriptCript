""" 
    This module is responsible for managing the creation, deletion, edition and user login.
"""

from flask import Flask, jsonify, make_response, request
from src.mariaDB.query_users import user_exists
from src.mariaDB.connection import get_db_connection
from src.utils.HashManager import HashManager
from flask import Blueprint
import logging
logging.basicConfig(level=logging.DEBUG)

challenges_bp = Blueprint('challenges', __name__)

@challenges_bp.route('/create_challenge', methods=['GET'])
def create_challenge():
    """Creates a new challenge in the database

    Return: returns a response object
    """
    data = request.get_json()
    title = data.get('title')
    document = data.get('document')
    userToShare = data.get('userToShare')
    userLogged = data.get('userLogged')
    
    hashedUser = HashManager.create_hash(userLogged)
    if not user_exists(hashedUser):
        response = make_response(
            jsonify({"response": "There is no creator user in the DB!"}), 422
        )
        return response
    
    hashedToShareUser = HashManager.create_hash(userToShare)
    if not user_exists(hashedToShareUser):
        response = make_response(
            jsonify({"response": "There is no creator user in the DB!"}), 422
        )
        return response
    
    #TODO: create AES method
    cipheredDocument = cipherAES(document)
    cipheredTitle = cipherAES(title)
    
    #TODO: insert challenge into database
    if insert_challenge(cipheredTitle, cipheredDocument, hashedUser, hashedToShareUser):
            response = make_response(jsonify({"response": "Challenge inserted"}), 401)
            return response 
    
    else:
        response = make_response(jsonify({"response": "Upps, something went wrong"}), 422)
        return response        

    
