import hashlib


class HashManager:
    """
    HashManager class is responsible for managing the creation of hashes using
    Sha256.

    + create_hash: Creates a sha256 hash from cleartext
    +  verify_hash: Verifies that two hashes are equal

    """

    def __init__(self):
        pass

    @staticmethod
    def create_hash(clear_text: str) -> str:
        """
        Create a hash of the password
        :param password -> password to hash
        :return -> hash of the password
        """
        return hashlib.sha256(clear_text.encode()).hexdigest()

    @staticmethod
    def verify_hash(clear_text: str, hash: str) -> bool:
        """
        Verify the inputted password against it's hash:
        :param password -> password to verify
        :param hash -> hash to verify against
        :return ->  True if hash matches password, False otherwise
        """
        return HashManager.create_hash(clear_text) == hash
