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
) -> bool:
    try:
        connection = get_digital_sign_db_connection()
        cursor = connection.cursor()
        query = f"SELECT encrypted_private_key FROM {DATABASE_DIGITAL_SIGN_NAME}.secure_keys WHERE username = %s;"
        cursor.execute(query, (hashed_user,))
        rows = cursor.fetchall()
        if len(rows) > 0:
            return True
        else: 
            return False
    except mysql.connector.Error as e:
        return False

    except Exception as e:
        return False
