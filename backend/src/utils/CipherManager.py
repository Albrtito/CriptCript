from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
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
        param - lengthKey: length of the desired key in bytes
        """
        #recover the password, which will act as a key
        password = get_user_password(user)
        expandedKey = CipherManager.hkdf_expand(password)

        cipher = Cipher(algorithms.AES(expandedKey), modes.ECB(), backend=default_backend()) # CAREFUL, WE ARE USING ECB
        encryptor = cipher.encryptor()

        logging.debug("Length of challenge is: %d", len(challenge))
        encrypted = encryptor.update(challenge.encode()) + encryptor.finalize()

        return base64.b64encode(encrypted).decode()
    
    @staticmethod
    def decipherChallengeAES(user, encrypted_challenge):
        """
        Deciphers a challenge using AES
        param - user: must be a hashed user
        param - encrypted_challenge: base64 encoded encrypted message
        """
        # Recover the password, which will act as a key
        password = get_user_password(user)
        expandedKey = CipherManager.hkdf_expand(password)
        logging.debug('Expanded key is %s of length: ', expandedKey, len(expandedKey))

        # Decode the base64 encoded encrypted message
        encrypted_challenge_bytes = base64.b64decode(encrypted_challenge)

        cipher = Cipher(algorithms.AES(expandedKey), modes.ECB(), backend=default_backend())
        decryptor = cipher.decryptor()

        # Decrypt the message directly
        decrypted = decryptor.update(encrypted_challenge_bytes) + decryptor.finalize()

        return decrypted
