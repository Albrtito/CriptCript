import logging

import mysql.connector
from src.mariaDB.connection import DATABASE_NAME, get_db_connection

def user_exists(hashed_user) -> bool:
    """Checks if a determined user exists
    hashed_user: a hashed_user
    Return: boolean
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = f"SELECT * FROM {DATABASE_NAME}.users WHERE username = %s"
        cursor.execute(query, (hashed_user,))
        rows = cursor.fetchall()
        if len(rows) > 0:
            return True
        else: 
            return False
    except mysql.connector.Error as e:
        logging.error(f"MySQL error: {e}")
        return False

    except Exception as e:
        logging.exception(f"Exception: {e}")
        return False
    
def insert_user(hashed_user, hashed_password) -> bool:
    """
    Insert a new user in the database given the hashed user and password.
    """
    # TODO: Check if the user alread exists in the database
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # TODO: Esta query esta deprecada. Es del modelo inicial del boilerplate
        query = f"INSERT INTO {DATABASE_NAME}.users VALUES (%s, %s)"
        cursor.execute(query, (hashed_user, hashed_password))
        connection.commit()

    except mysql.connector.Error as e:
        logging.error(f"MySQL error: {e}")
        return False

    except Exception as e:
        logging.exception(f"Exception: {e}")
        return False

    return True


def get_user_password(hashed_user) -> str:
    """
    Get the hashed password of a user given the hashed user.
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # TODO: Esta query hay que cambiarla para que la función funcione
        query = "SELECT user_password FROM users where username = %s"
        cursor.execute(query, (hashed_user,))
        rows = cursor.fetchall()
        logging.debug(rows)
        if rows:
            hashed_password = rows[0][0]
        
    except mysql.connector.Error as e:
        logging.error(f"MySQL error: {e}")
        return None
    
    except Exception as e:
        logging.exception(f"Exception: {e}")
        return  None
    
    return hashed_password 
