""" 
    This module is responsible for managing the creation, deletion, edition and user login.
"""

import logging

from flask import Blueprint, Flask, jsonify, make_response, request
from src.mariaDB.query_challenges import (insert_challenge, return_all_public,
                                          return_shared_with_user)
from src.utils.CipherManager import CipherManager
from src.utils.HashManager import HashManager
from src.utils.keys import KeyGen
from src.utils.MessageManager import MessageManager

logging.basicConfig(level=logging.DEBUG)

challenges_bp = Blueprint("challenges", __name__)


@challenges_bp.route("/create_challenge", methods=["POST"])
def create_challenge():
    """Creates a new challenge in the database
    Return: returns a response object
    """
    data = request.get_json()
    title = data.get("title")
    document = data.get("document")
    userToShare = data.get("userToShare")
    userLogged = data.get("userLogged")

    # Check that there is a logged user
    if len(userLogged) == 0:
        response = make_response(jsonify({"response": "There is no user logged"}), 422)
        return response

    # Hash the value of the user to obtain the reference in the db
    hashedUser = HashManager.create_hash(userLogged)

    # Check if the challenge is public or private

    if (
        len(userToShare) == 0
    ):  # if challenge is public, cypher it with admin password hash
        # NOTE: This is not the best practice. Later on with the implementation
        # of the KeyGen class this will change.

        # Get user hash and the key from KeyGen class
        adminHash = HashManager.create_hash("admin")
        key = KeyGen.key_from_user(adminHash, 256)

        # cipheredTitle = CipherManager.cipherChallengeAES(adminHash, title)
        # cipheredMessage = CipherManager.cipherChallengeAES(adminHash, document)
        cipheredTitle = MessageManager.cipher_message(title, key)
        cipheredMessage = MessageManager.cipher_message(document, key)

        # Insert the ciphered challenge into the db
        insert_challenge(cipheredTitle, hashedUser, cipheredMessage, False)

        response = make_response(
            jsonify({"response": "Challenge has been created!"}), 201
        )
        return response

    else:
        userHash = HashManager.create_hash(userToShare)
        key = KeyGen.key_from_user(userHash, 256)

        # cipheredTitle = CipherManager.cipher_message(userHash, title)
        # cipheredMessage = CipherManager.cipherChallengeAES(userHash, document)
        cipheredTitle = MessageManager.cipher_message(title, key)
        cipheredMessage = MessageManager.cipher_message(document, key)

        insert_challenge(cipheredTitle, hashedUser, cipheredMessage, True, userHash)

        response = make_response(
            jsonify({"response": "Challenge has been created!"}), 201
        )
        return response


@challenges_bp.route("/get_public_challenges", methods=["GET"])
def get_public_challenges():
    """
    Returns a response with all public challenges available for the user
    """
    publicChallenges = return_all_public()
    response = []
    # remember: the key was the extended admin password (hash)
    hashed_user = HashManager.create_hash("admin")
    key = KeyGen.key_from_user(hashed_user)

    # fields to decipher: title = 1, content = 2, author = 3, where numbers = index in the array
    for i in range(0, len(publicChallenges), 1):  # iterate through every row
        cipheredTitle = publicChallenges[i][1]
        cipheredContent = publicChallenges[i][3]

        # title = CipherManager.decipherChallengeAES(hashed_user, cipheredTitle)
        # content = CipherManager.decipherChallengeAES(hashed_user, cipheredContent)
        title = MessageManager.decipher_message(cipheredTitle, key)
        content = MessageManager.decipher_message(cipheredContent, key)

        json = {"title": title, "content": content}
        response.append(json)
    response = make_response(jsonify({"response": response}), 201)
    return response


@challenges_bp.route("/get_private_challenges", methods=["GET"])
def get_private_challenges():
    """
    Returns a response with all the private challenges shared with an user
    """
    user = request.args.get("user")
    user_hash = HashManager.create_hash(user)  # obtain the hashed user for the query
    key = KeyGen.key_from_user(user_hash)
    privateChallenges = return_shared_with_user(user)
    response = []

    for i in range(0, len(privateChallenges), 1):
        cipheredTitle = privateChallenges[i][1]
        cipheredContent = privateChallenges[i][3]

        #title = CipherManager.decipherChallengeAES(user, cipheredTitle)
        #content = CipherManager.decipherChallengeAES(user, cipheredContent)
        title = MessageManager.decipher_message(cipheredTitle,key)
        content = MessageManager.decipher_message(cipheredContent,key)

        json = {"title": title, "content": content}
        response.append(json)

    response = make_response(jsonify({"response": response}))
    return response
