import logging

logging.basicConfig(level=logging.DEBUG)
import mysql.connector
from src.mariaDB.connection import DATABASE_DIGITAL_SIGN_NAME, get_digital_sign_db_connection


def insert_secure_keys(
    username: str,
    encrypted_private_key: bytes,
    public_key: str
) -> bool:
    """
    Inserts digital firm keys for each user registered
    """
    try:
        connection = get_digital_sign_db_connection()
        cursor = connection.cursor()

        query = f"INSERT INTO {DATABASE_DIGITAL_SIGN_NAME}.secure_keys(username, encrypted_private_key, public_key) VALUES (%s, %s, %s)"
        cursor.execute(
            query, (username, encrypted_private_key, public_key)
        )

        connection.commit()

    except mysql.connector.Error as e:
        logging.debug("%s", e)
        return False

    except Exception as e:
        logging.debug("%s", e)
        return False
    return True

def get_private_ciphered_key(
    hashed_user: str
) -> bytes:
    try:
        connection = get_digital_sign_db_connection()
        cursor = connection.cursor()
        query = f"SELECT encrypted_private_key FROM {DATABASE_DIGITAL_SIGN_NAME}.secure_keys WHERE username = %s;"
        cursor.execute(query, (hashed_user,))
        rows = cursor.fetchall()
        return rows[0][0] # theorically it just can exist one item here
    except mysql.connector.Error as e:
        raise e

    except Exception as e:
        raise e
    
def get_public_key(
    hashed_user: str
):
    try:
        connection = get_digital_sign_db_connection()
        cursor = connection.cursor()
        query = f"SELECT public_key FROM {DATABASE_DIGITAL_SIGN_NAME}.secure_keys WHERE username = %s;"
        cursor.execute(query, (hashed_user,))
        rows = cursor.fetchall()
        return rows[0][0] # theorically it just can exist one item here
    except mysql.connector.Error as e:
        return []

    except Exception as e:
        return []

def insert_signature_in_db(
    message: bytes,
    signature: bytes
):
    try:
        connection = get_digital_sign_db_connection()
        cursor = connection.cursor()
        query = f"INSERT INTO {DATABASE_DIGITAL_SIGN_NAME}.digital_signatures(content, signature) VALUES (%s, %s)"
        cursor.execute(
            query, (message, signature)
        )
        connection.commit()
    except mysql.connector.Error as e:
        logging.debug(e)
        return False

    except Exception as e:
        logging.debug(e)
        return False

    return True

def get_signature(cipheredMessage: bytes):
    try:
        connection = get_digital_sign_db_connection()
        cursor = connection.cursor()
        query = f"SELECT signature FROM {DATABASE_DIGITAL_SIGN_NAME}.digital_signatures WHERE content = %s;"
        cursor.execute(query, (cipheredMessage,))
        rows = cursor.fetchall()
        return rows[0][0] # theorically it just can exist one item here
    except mysql.connector.Error as e:
        return []

    except Exception as e:
        return []
