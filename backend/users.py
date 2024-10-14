from flask import Blueprint, request, jsonify, make_response
import mysql.connector
import logging
from .database import get_db_connection

users_bp = Blueprint('users', __name__)

@users_bp.route('/get-users', methods=['GET'])
def get_users():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        query = "SELECT * FROM users"
        cursor.execute(query)
        rows = cursor.fetchall()
        
    except mysql.connector.Error as e:
        logging.error(f"MySQL error: {e}")
        response = make_response(jsonify({'response': 'Users could not be obtained'}), 400)
        return response
    
    except Exception as e:
        logging.exception(f"Exception: {e}")
        response = make_response(jsonify({'response': 'Users could not be obtained'}), 400)
        return response
    
    response = make_response(jsonify({"response": rows}), 201)
    return response

@users_bp.route('/insert-user', methods=['POST'])
def insert_user():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, email, password))
        connection.commit()
        
    except mysql.connector.Error as e:
        logging.error(f"MySQL error: {e}")
        response = make_response(jsonify({'response': 'User could not be inserted'}), 400)
        return response
    
    except Exception as e:
        logging.exception(f"Exception: {e}")
        response = make_response(jsonify({'response': 'User could not be inserted'}), 400)
        return response
    
    response = make_response(jsonify({"response": "User inserted successfully!"}), 201)
    return response

@users_bp.route('/delete-user', methods=['DELETE'])
def delete_user():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        data = request.get_json()
        user_to_remove = data.get('user')
        
        query = "DELETE FROM users WHERE username = %s"
        cursor.execute(query, (user_to_remove,))
        connection.commit()
        
    except mysql.connector.Error as e:
        logging.error(f"MySQL error: {e}")
        response = make_response(jsonify({'response': 'User could not be deleted'}), 400)
        return response
    
    except Exception as e:
        logging.exception(f"Exception: {e}")
        response = make_response(jsonify({'response': 'User could not be deleted'}), 400)
        return response
    
    response = make_response(jsonify({'response': 'User was successfully deleted!'}), 200)
    return response
