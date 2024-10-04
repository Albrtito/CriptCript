import hashlib

class HashManager:
    """
    HashManager class is responsible for managing the creation,verification and comparison of hashes
    """
    def __init__(self):
        pass

    def create_hash(self, password):
        """
        Create a hash of the password
        :param password -> password to hash
        :return -> hash of the password
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_hash(self, password, hash) -> bool:
        """
        Verify the inputted password against it's hash:
        :param password -> password to verify
        :param hash -> hash to verify against
        :return ->  True if hash matches password, False otherwise 
        """
        return self.create_hash(password) == hash
