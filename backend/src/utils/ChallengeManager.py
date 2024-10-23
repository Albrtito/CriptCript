class ChallengeManager:
    """
    ChallengeManager class is responsible for defining all ciphering and deciphering functions for the challenges.
    """
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def caesar_cipher(message: str) -> dict:
        """
        Used for ciphering a challenge text with the Caesar Cipher (n_rotation = 3).
        
        :param message: The message to be ciphered.
        :return: A dictionary with the ciphered alphabet and the ciphered message.
        """
        n_rotation = 3  # Fixed rotation value
        alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'ñ', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        
        if len(message) == 0:
            raise ValueError("Error: The message cannot be empty.")

        # Creating the ciphered alphabet
        cipheredAlphabet = []
        counter = 0
        
        # Add the rotated part of the alphabet
        while counter < len(alphabet) - n_rotation:
            cipheredAlphabet.append(alphabet[counter + n_rotation])
            counter += 1
        
        # Add the remaining positions
        for i in range(n_rotation):
            cipheredAlphabet.append(alphabet[i])
        
        # Mapping between original alphabet and ciphered alphabet
        nomenclator = {alphabet[i]: cipheredAlphabet[i] for i in range(len(alphabet))}
        
        # Prepare the message for ciphering (lowercase, no spaces)
        messageToCipher = message.lower().replace(" ", "")
        cipheredMessage = ''.join([nomenclator[char] for char in messageToCipher])
        
        if len(cipheredMessage) != len(messageToCipher):
            raise ValueError("Error: Something went wrong during ciphering, message lengths do not match.")
        
        return {'cipheredAlphabet': cipheredAlphabet, 'cipheredMessage': cipheredMessage}
