import logging
logging.basicConfig(level=logging.DEBUG)
import mysql.connector
from src.mariaDB.connection import DATABASE_CERTIFICATES_NAME, get_certificate_db_connection

def insert_certificate(
    user: str,
    encrypted_private_key: bytes,
    certificate_blob: bytes,
) -> bool:
    """
    Inserts a certificate into the database.
    """
    try:
        connection = get_certificate_db_connection()
        cursor = connection.cursor()
        
        query = f"INSERT INTO {DATABASE_CERTIFICATES_NAME}.user_certificates(username, encrypted_private_key, certificate_blob) VALUES (%s, %s, %s)"
        
        cursor.execute(query, (user, encrypted_private_key, certificate_blob))
        connection.commit()

    except mysql.connector.Error as e:
        logging.debug("%s", e)
        return False

    except Exception as e:
        logging.debug("%s", e)
        return False
    
    return True
