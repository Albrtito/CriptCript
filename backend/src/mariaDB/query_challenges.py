import logging
import mysql.connector
from src.mariaDB.connection import DATABASE_NAME, get_db_connection

def insert_challenge(hashed_name_challenge, hash_creator_user, hash_content, isPrivate, hashed_shared_user='') -> bool:
    """
    Inserts a hashed challenge
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        if not isPrivate:
            query = f"INSERT INTO {DATABASE_NAME}.public_challenges (name_challenge, user, content) VALUES (%s, %s, %s)"        
            cursor.execute(query, (hashed_name_challenge, hash_creator_user, hash_content))
            connection.commit()
        else:
            query = f"INSERT INTO {DATABASE_NAME}.private_challenges (name_challenge, user, content, shared_user) VALUES (%s, %s, %s, %s)"        
            cursor.execute(query, (hashed_name_challenge, hash_creator_user, hash_content, hashed_shared_user))
            connection.commit()
    except mysql.connector.Error as e:
        logging.debug("%s", e)
        return False

    except Exception as e:
        logging.debug("%s", e)
        return False
    return True

def return_all_public():
    """
    Returns all possible public challenges
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM public_challenges"
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows:
            return rows

    except mysql.connector.Error as e:
        return None
    except Exception as e:
        return  None