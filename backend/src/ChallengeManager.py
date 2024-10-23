""" 
    This module is responsible for managing the creation, deletion, edition and user login.
"""

from flask import Flask, jsonify, make_response, request
from src.mariaDB.query_users import insert_user, get_user_password
from src.utils.HashManager import HashManager
from flask import Blueprint
import logging
logging.basicConfig(level=logging.DEBUG)

challenges_bp = Blueprint('challenges', __name__)

@challenges_bp.route('/create_challenge', methods=['GET'])
def hello():
    """Creates a new challenge in the database

    Return: returns a response object
    """
    data = request.get_json()
    title = data.get('title')
    document = data.get('document')
    userToShare = data.get('userToShare')
    userLogged = data.get('userLogged')
    
