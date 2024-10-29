from cryptography.hazmat.primitives import hashes, hmac


class MACManager:
    """
    This class contains all methods related to creating and verifying MAC
    encription. 
    
    HMAC:
    + create_HMAC: Create an HMACs based on sha256
        + cleartext: For MAC-THEN-ENCRIPT
        + ciphered: For ENCRIPT-THEN-MAC 
    + verify_HMAC: Verifies an HMAC
        + cleartext: For MAC-THEN-ENCRIPT
        + ciphered: For ENCRIPT-THEN-MAC 
    """

    def __init__(self) -> None:
        pass

    @staticmethod
    def create_cleartext_HMAC(data:str, key: str) -> bytes:
        """
        Creates an HMAC based on the key, data and algorithm defined.
        + The algorithm is always sha256
        """
        # Convert the data and key to bytes
        data_bytes = data.encode()
        key_bytes = key.encode()
        
        # Define the object that creates the HMAC - Object of type HashContex
        hmac_creator = hmac.HMAC(key_bytes, hashes.SHA256())

        # Create the HMAC hash:
        hmac_creator.update(data_bytes)
        hmac_value = hmac_creator.finalize()

        return hmac_value 

    @staticmethod
    def create_ciphered_HMAC(ciphered_data:bytes, key: str) -> bytes:
        """
        Creates an HMAC based on the key, data and algorithm defined.
        + The algorithm is always sha256
        """
        # Convert the data and key to bytes
        key_bytes = key.encode()
        
        # Define the object that creates the HMAC - Object of type HashContex
        hmac_creator = hmac.HMAC(key_bytes, hashes.SHA256())

        # Create the HMAC hash:
        hmac_creator.update(ciphered_data)
        hmac_value = hmac_creator.finalize()

        return hmac_value 

    @staticmethod
    def verify_cleartext_HMAC(data:str, key:str, hmac_value:bytes) -> bool:
        """
        Verifies the HMAC valeu for some key and some data
        """

        # Convert the data and key to bytes
        data_bytes = data.encode()
        key_bytes = key.encode()

        # Define the object that verifies the HMAC: Object of type HashContex
        hmac_verifier =  hmac.HMAC(key_bytes, hashes.SHA256())

        # Verify the HMAC hash:
        hmac_verifier.update(data_bytes)
        try: 
            hmac_verifier.verify(hmac_value)
            return  True
        except:
            raise ValueError("The HMAC is not correct") 

    @staticmethod
    def verify_ciphered_HMAC(ciphered_data:bytes , key:str, hmac_value:bytes) -> bool:
        """
        Verifies the HMAC valeu for some key and some data
        """

        # Convert the data and key to bytes
        key_bytes = key.encode()

        # Define the object that verifies the HMAC: Object of type HashContex
        hmac_verifier =  hmac.HMAC(key_bytes, hashes.SHA256())

        # Verify the HMAC hash:
        hmac_verifier.update(ciphered_data)
        try: 
            hmac_verifier.verify(hmac_value)
            return  True
        except:
            raise ValueError("The HMAC is not correct") 
        




