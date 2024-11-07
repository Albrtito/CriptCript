import logging
logging.basicConfig(level=logging.DEBUG)
import mysql.connector
from src.mariaDB.connection import DATABASE_NAME, get_db_connection

def insert_challenge(hashed_name_challenge:bytes, hash_creator_user:str,
                     hash_content:bytes,
                     isPrivate:bool,auth=None, hashed_shared_user='') -> bool:
    """
    Inserts a hashed challenge
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        if not isPrivate:
            query = f"INSERT INTO {DATABASE_NAME}.public_challenges(name_challenge, user,content,auth) VALUES (%s, %s,%s,%s)"        
            cursor.execute(query, (hashed_name_challenge, hash_creator_user,hash_content,auth))
            connection.commit()
        else:
            query = f"INSERT INTO {DATABASE_NAME}.private_challenges(name_challenge, user, content,auth, shared_user) VALUES (%s,%s, %s, %s, %s)"        
            cursor.execute(query, (hashed_name_challenge, hash_creator_user,hash_content,auth ,hashed_shared_user))
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
        return [] 
    except Exception as e:
        return [] 
    
def return_shared_with_user(user):
    """
    Returns all challenges shared with the user
    param user - a hashed user
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM private_challenges WHERE shared_user = %s;"
        cursor.execute(query, (user,))
        rows = cursor.fetchall()
        
        if rows:
            return rows
        
    except mysql.connector.Error as e:
        return []
    except Exception as e:
        return  []
