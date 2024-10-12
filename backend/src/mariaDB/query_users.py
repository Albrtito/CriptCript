import logging

import mysql.connector
from mariaDB.connection import DATABASE_NAME, get_db_connection


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
        query = "SELECT * FROM users"
        cursor.execute(query)
        rows = cursor.fetchall()
        #TODO: Aquí tiene que terminar la contraseña hasheada.
        hashed_password = None
        
    except mysql.connector.Error as e:
        logging.error(f"MySQL error: {e}")
        return None
    
    except Exception as e:
        logging.exception(f"Exception: {e}")
        return  None
    
    return hashed_password 
