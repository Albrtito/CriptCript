""" 
    This module is responsible for managing the creation, deletion, edition and user login.
"""

from flask import Flask, jsonify, make_response, request
from utils.HashManager import HashManager
from MariaDb.user import insert_user

# NOTE:ESTO HAY QUE ENRUTARLO
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

    if insert_user(hashed_user, hashed_password):
        # En el caso de que el hash no exista devolvemos un mensaje de éxito
        response = make_response(
            jsonify({"response": "User created successfully!"}), 201
        )
    else:
        # En el caso de que el hash ya exista, devolvemos un error
        response = make_response(jsonify({"response": "Username already exists"}), 201)

    return response
