import logging

from src.utils.auth import *
from src.utils.encryption import *
from src.mariaDB.query_users import get_user_password
from src.utils.auth.MACManager import MACManager
from src.utils.encryption.AESManager import AESManager

logging.basicConfig(level=logging.DEBUG)


# TODO: Conseguir que cada usuario pueda decidir en ajustes que tipo de cifrado
# quiere usar, basándonos en eso configurar el los métodos de cifrado y
# autenticación de esta clase
class MessageManager:
    """
    This class encripts and authenticates a message using the tools configured
    this encription can be done in one of two ways:

    1. Using two sepparate tools, one for encription(see under:
    src/utils/encryption) and another one for authentication(see under
    src/utils/auth)

    2. Using one unified tool (Cifrado autenticado), (see under:
    src/utils/authEncryption)

    METHODS:
    + cipher_message: Cipher a message given an encription algorithm
    + decipher_message: Decipher a message given an encription algorithm
    + auth_create: Creates the auth code for a message
    + auth_verify: Verifies the authenticity of a message

    TODO: 
    + obtain_settings: Get the method used for encription, decription of a
    message

    NOTES:
    Right now the encription of messages is done using AES and the
    authentication of them using HMAC. All of it uses sha256 as hashing
    algorithm.
    """
    

    def __init__(self) -> None:
        pass

    @staticmethod
    def cipher_message(message:str,key:str,ENCRYPTION_TYPE = "AES") -> bytes:
        """
        Cipher a given a message, a key and an algorithm 
        NOTE: See comments in KeyGen for future changes

        :param message -> Cleartext string message
        :param key -> String value of the key to cipher
        :param ENCRYPTION_TYPE -> Type of algorithm used to cipher
        :return -> Ciphered bytes
        """

        try: 
            logging.info
            (
                f"""
                ---------
                Message being ciphered: {message}
                Key used: {key}
                ---------
                """
            )
            ciphered_message = AESManager.encript_AES(message, key)        
            logging.info
            (
                f"""
                ---------
                Message ciphered: {ciphered_message}
                Key used: {key}
                ---------
                """
            )
            return ciphered_message
        except:
            logging.warning("Problem while ciphering a message")
            raise Exception("Could not cipher message") 


        
    @staticmethod
    def decipher_message(ciphered_message:bytes,key:str, ENCRIPTION_TYPE = "AES") ->str:
        """
        Decipher a given message, a key and an algorithm 
        NOTE: See comments in KeyGen for future changes

        :param ciphered_message -> Ciphered message in bytes
        :param key -> String value of the key to cipher
        :param ENCRYPTION_TYPE -> Type of algorithm used to cipher
        :return -> Cleartext string
        """

        try: 
            logging.info
            (
                f"""
                ---------
                Message being deciphered: {ciphered_message}
                Key used: {key}
                ---------
                """
            )
            message = AESManager.decript_AES(ciphered_message, key)        
            logging.info
            (
                f"""
                ---------
                Message deciphered: {message}
                Key used: {key}
                ---------
                """
            )
            return message 
        except:
            logging.warning("Problem while deciphering a message")
            raise Exception("Could not decipher message") 

    @staticmethod
    def auth_create(ciphered_message:bytes,key:str,AUTH_TYPE = "HMAC") -> bytes:
        """
        Creates an authentication code for ciphered messages.
        NOTE: Using the ENCRIPT-THEN-MAC approach

        :param ciphered_message -> Ciphered message in bytes
        :param key -> String value of the key to cipher
        :param AUTH_TYPE -> Type of algorithm used to authenticate
        """

        try: 
            logging.info
            (
                f"""
                ---------
                Auth bein created: {ciphered_message}
                Key used: {key}
                ---------
                """
            )
            auth = MACManager.create_ciphered_HMAC(ciphered_message, key)        
            logging.info
            (
                f"""
                ---------
                Auth created: {auth}
                Key used: {key}
                ---------
                """
            )
            return auth 
        except:
            logging.warning("Problem while creating auth")
            raise Exception("Could not create auth for message") 



    @staticmethod
    def auth_verify(MAC:bytes, ciphered_message:bytes, key:str, AUTH_TYPE= "HMAC") -> bool:
        """
        Checks the authenticity of a ciphered message
        NOTE: Using the ENCRIPT-THEN-MAC approach

        :param MAC -> MAC value to verify
        :param ciphered_message -> Ciphered message in bytes
        :param key -> String value of the key to cipher
        :param AUTH_TYPE -> Type of algorithm used to authenticate
        """

        try: 
            logging.info
            (
                f"""
                ---------
                Auth bein verified: {MAC}
                Cipherd message: {ciphered_message}
                Key used: {key}
                ---------
                """
            )
            verify = MACManager.verify_ciphered_HMAC(ciphered_message,key, MAC)
            logging.info
            (
                f"""
                ---------
                Verified mac: {MAC}
                Key used: {key}
                result: {verify}
                ---------
                """
            )
            return verify 

        except:

            logging.warning("Problem while verifying auth")
            raise Exception("Could not verify auth for message") 


