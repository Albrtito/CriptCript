from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

from src.utils.keys import KeyGen

# TODO: Se podría pensar en hacer que esta clase tuviese el cifrado directamente
# implementado al crear la clase, de esta forma se crearía un instance de la calse para cada cifrado.
class AESManager:

    """
    This class contains all the methods related with AES encryption and
    decryption.
    NOTE: Because this class is not implementing authenticated encryption it'll
    use AES CTR mode.

    + encript_AES: Ciphers a message with AES
    + decript_AES: Deciphers a message with AES

    """

    def __init__(self) -> None:
        pass

    @staticmethod
    def encript_AES(data: str, key: bytes, nonce=KeyGen.new_nonce())-> bytes:
        """
        Encrypts the data with the key using AES
        :param data: The data to be encrypted
        :param key: The key to encrypt the data.
            - Either 128, 192 or 256 BITS
        :param nonce: Value for the nonce(CTR mode)
        :return: The encrypted data
        """
        
        data_bytes = data.encode()
        key_bytes = key

        # Create the AES cipher:
        cipher = Cipher(algorithms.AES(key_bytes), modes.CTR(nonce))
        # Create the encriptor. Messages going though it will be ciphered with
        # the cipher generated above.
        encryptor = cipher.encryptor()

        # Cipher the message:
        ciphered_data = encryptor.update(data_bytes) + encryptor.finalize()
        ciphered_data = nonce + ciphered_data

        # Rerturn the ciphered message
        return ciphered_data

    @staticmethod
    def decript_AES(encrypted_data: bytes, key: bytes) -> str:
        """
        Decrypts the data with the key using AES
        :param data: The data to be decrypted
        :param key: The key to decrypt the data
        :return: The decrypted data
        
        """
        # Convert the key to bytes
        key_bytes = key
        # Obtain the value for the nonce from the message
        nonce = encrypted_data[:16]
        # Substract the noncec from the encrypted data
        encrypted_data = encrypted_data[16:]

        # Create the AES cipher:
        cipher = Cipher(algorithms.AES(key_bytes), modes.CTR(nonce))

        # Create the encriptor. Messages going though it will be ciphered with
            # the cipher generated above.
        decryptor = cipher.decryptor()

        # Cipher the message:
        data = decryptor.update(encrypted_data) + decryptor.finalize()

        # Rerturn the ciphered message, decoded as a string

        return data.decode()
