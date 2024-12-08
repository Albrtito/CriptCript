import mysql.connector
from src.mariaDB.connection import DATABASE_KEYS_NAME, get_keys_db_connection


def insert_salt_in_db(
    ciphered_challenge: bytes,
    salt: bytes,
) -> bool:
    """
    Inserts a key into the database.
    :param ciphered_challenge: Ciphered text of the cahllenge in bytes
    :param salt: salt in bytes
    """

    # Insert the values into the database:
    try:
        connection = get_keys_db_connection()
        cursor = connection.cursor()

        query = f"INSERT INTO {DATABASE_KEYS_NAME}.salt_challenges\
        (ciphered_challenge, salt) VALUES (%s, %s)"

        cursor.execute(query, (ciphered_challenge , salt))
        connection.commit()

        return True

    except mysql.connector.Error as e:
        return False

    except Exception as e:
        return False

def get_salt_from_db(
    ciphered_challenge: bytes,
) -> bytes|None:
    """
    Given a challenge_id, challenge_type and key_type, returns the key stored
    in the database.
    :param challenge_id: Id of the challenge. The one that the key is related to
    :param challenge_type: Type of the challenge (Public or Private)
    :param key_type: Type of the key based on the algorithm used (AES, FERNET)
    :return: Key in bytes
           : None if the key is not found
    """
    connection = None
    cursor = None
    try:
        connection = get_keys_db_connection()
        cursor = connection.cursor()
        
        query = """
            SELECT salt 
            FROM {}.salt_challenges 
            WHERE ciphered_challenge = %s
        """.format(DATABASE_KEYS_NAME)
        
        cursor.execute(query, (ciphered_challenge,))
        rows = cursor.fetchall()
        
        return rows[0][0] if rows else None
        
    except mysql.connector.Error as e:
        raise ValueError(f"Database error occurred: {str(e)}") from e
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

