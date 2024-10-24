import logging
import hashlib


class HashManager:
    """
    HashManager class is responsible for managing the creation,verification and comparison of hashes
    """
    def __init__(self):
        pass
    @staticmethod
    def create_hash( clear_text) -> str:
        """
        Create a hash of the password
        :param password -> password to hash
        :return -> hash of the password
        """
        return hashlib.sha256(clear_text.encode()).hexdigest()
   
    @staticmethod
    def verify_hash( clear_text, hash) -> bool:
        """
        Verify the inputted password against it's hash:
        :param password -> password to verify
        :param hash -> hash to verify against
        :return ->  True if hash matches password, False otherwise 
        """
        return HashManager.create_hash(clear_text) == hash
