import logging
import mysql.connector
from src.mariaDB.connection import DATABASE_NAME, get_db_connection

def insert_challenge(hashed_name_challenge, hash_creator_user, hash_content, isPrivate, hashed_shared_user) -> bool:
    """
    Inserts a hashed challenge
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = f"INSERT INTO {DATABASE_NAME}.challenges (name_challenge, user, content, isPrivate, shared_user) VALUES (%s, %s, %s, %s, %s)"        
        cursor.execute(query, (hashed_name_challenge, hash_creator_user, hash_content, isPrivate, hashed_shared_user))
        connection.commit()
    except mysql.connector.Error as e:
        logging.debug("%s", e)
        return False

    except Exception as e:
        logging.debug("%s", e)
        return False
    return True