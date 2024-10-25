from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

import hashlib
import base64
from src.mariaDB.query_users import get_user_password
import logging
logging.basicConfig(level=logging.DEBUG)

class CipherManager():
    """
    This class contains all the methods related with ciphering
    """
    def __init__(self) -> None:
        pass

    @staticmethod
    def hkdf_expand(passwordHash, length=16, salt=b'', info=b''):
        """
        Given a hash, it expands it. Lenght is considered to be in BYTES 16 bytes = 128bits
        """
        passwordBytes = passwordHash.encode()
        hkdf = hashlib.pbkdf2_hmac('sha256', passwordBytes, salt, 100000, dklen=length)
        return hkdf

    @staticmethod
    def cipherChallengeAES(user, challenge):
        """
        Ciphers a challenge using AES
        param - user: must be a hashed user
        param - challenge: plain text message
        """
        # Recupera la contraseña, que actuará como clave
        password = get_user_password(user)
        expandedKey = CipherManager.hkdf_expand(password)

        # Configura el cifrado AES con ECB
        cipher = Cipher(algorithms.AES(expandedKey), modes.ECB(), backend=default_backend())
        encryptor = cipher.encryptor()

        # Relleno del challenge para que tenga el tamaño adecuado
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(challenge.encode()) + padder.finalize()

        logging.debug("cipherChallengeAES>>>>Type of padded data: %s. Content of padded data: %s", type(padded_data), padded_data)

        # Cifra el texto rellenado
        encrypted = encryptor.update(padded_data) + encryptor.finalize()
        
        logging.debug("cipherChallengeAES>>>>Type of encrypted: %s. Content of encrypted: %s", type(encrypted), encrypted)

        return encrypted
    
    @staticmethod
    def decipherChallengeAES(user, encrypted_challenge):
        """
        Deciphers a challenge using AES
        param - user: must be a hashed user
        param - encrypted_challenge: bytes encoded encrypted message
        """
        # Recupera la contraseña, que actuará como clave
        password = get_user_password(user)
        expandedKey = CipherManager.hkdf_expand(password)

        # Configura el cifrado AES con ECB
        cipher = Cipher(algorithms.AES(expandedKey), modes.ECB(), backend=default_backend())
        decryptor = cipher.decryptor()

        # Descifra el mensaje
        decrypted = decryptor.update(encrypted_challenge) + decryptor.finalize()

        # Quita el relleno
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        unpadded_data = unpadder.update(decrypted) + unpadder.finalize()

        deciphered_output = unpadded_data.decode('utf-8')

        logging.debug("decipherChallengeAES>>>>Type of decrypted: %s. Content of decrypted: %s", type(deciphered_output), deciphered_output)

        return deciphered_output

