""" 
    This module is responsible for managing the creation, deletion, edition and user login.
"""

from flask import Flask, jsonify, make_response, request
from src.mariaDB.query_users import user_exists, get_user_password
from src.mariaDB.query_challenges import insert_challenge, return_all_public
from src.utils.HashManager import HashManager
from src.utils.CipherManager import CipherManager
from flask import Blueprint
import logging
logging.basicConfig(level=logging.DEBUG)

challenges_bp = Blueprint('challenges', __name__)

@challenges_bp.route('/create_challenge', methods=['POST'])
def create_challenge():
    """Creates a new challenge in the database
    Return: returns a response object
    """
    data = request.get_json()
    title = data.get('title')
    document = data.get('document')
    userToShare = data.get('userToShare')
    userLogged = data.get('userLogged')
    
    if  len(userLogged) == 0:
            response = make_response(jsonify({"response": "There is no user logged"}), 422)
            return response
    
    hashedUser = HashManager.create_hash(userLogged)
    if len(userToShare) == 0: # if challenge is public, cypher it with admin password hash
          adminHash = HashManager.create_hash('admin') # unsafe as fuck, but what we can do...
          titleHash = HashManager.create_hash(title)
          documentHash = HashManager.create_hash(document)

          cipheredTitle = CipherManager.cipherChallengeAES(adminHash, titleHash)
          cipheredMessage = CipherManager.cipherChallengeAES(adminHash, documentHash)

          insert_challenge(titleHash, hashedUser, documentHash, 0, None)

          response = make_response(jsonify({"response": "Challenge has been created!"}), 201)
          return response 

    else:
          userHash = HashManager.create_hash(userToShare)
          titleHash = HashManager.create_hash(title)
          documentHash = HashManager.create_hash(document)
    
          cipheredTitle = CipherManager.cipherChallengeAES(userHash, titleHash)
          cipheredMessage = CipherManager.cipherChallengeAES(userHash, documentHash)

          insert_challenge(titleHash, hashedUser, documentHash, 1, userHash)

          response = make_response(jsonify({"response": {"title": cipheredTitle, "message": cipheredMessage, "userShared": userToShare, "userLogged": userHash}}), 201)
          return response 
    
@challenges_bp.route('/get_public_challenges', methods=['GET'])
def get_public_challenges():
      """
      Returns a response with all public challenges available for the user
      """
      publicChallenges = return_all_public()

      # fields to decipher: title = 1, content = 2, author = 3, where numbers = index in the array
      for i in range(0, len(publicChallenges), 1): # iterate through every row
            title = publicChallenges[i][1]
            content = publicChallenges[i][2]
            author = publicChallenges[i][3]
            
            # remember: the key was the extended admin password (hash)
            hashed_user = HashManager.create_hash('admin')
            title = CipherManager.decipherChallengeAES(hashed_user, title)
            logging.debug("title is: %s", title)
      response = make_response(jsonify({"response": publicChallenges}), 201)
      return response 