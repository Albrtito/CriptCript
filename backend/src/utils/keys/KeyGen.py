# TODO: Esta clase se encargará de generar claves y de saber que clave hay que
# usar para descifrar cada mensaje.

# NOTE: Que la clase MessageManger no tome un valor key:srt sino un objeto key
# de esta clase. Ese objeto se obtiene directamente por el mensaje que se queire
# descibrar o se crea al cifrar un mensaje.

#BUG: Esta implementación tiene un problema, si un usuario cambia su contraseña
#(por ahora no pueden) el cifrado de mensajes anteriores se pierde pues ya no se
#puede calcular la clave

#NOTE: Esta clase también ha de asegurar que las claves son de la longitud deseada
import os
import hashlib
from src.mariaDB.query_users import get_user_password
from src.mariaDB.query_challenges import get_len_challenges
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

def key_from_user(hashed_user: str, length=256) -> tuple:
    """
    Creates a key derived from the user hashed password.
    :param hashed_user -> String with the username (in hash form)
    :param lenght -> Lenght of the key to generate in BITS
    :return -> Return the value of the key created
    """
    # Generate a salt randomly. No need to save it.
    salt = os.urandom(16)
    # Get the current password of the user:
    user_password = get_user_password(hashed_user)
    # Derive a key from the user password
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=length // 8,
        salt=salt,
        iterations=100000,
    )
    key = kdf.derive(user_password.encode())
    key = key.encode()

    # The key must be 32 bits long so it can later turn into a 256 bit key.
    # Check
    if len(key) == (length // 8):
        return key,salt
    else:
        raise TypeError("The key doesn't have a valid size")



def new_nonce() -> bytes:
    """
    This function generates a new nonce for AES encription.
    It ensures that this nonce has never been used and has a len of 16 bytes. 
    To prevent repeating when the len of the challenges is greater than 16 we can perform a hash. 
    :return -> Nonce value (16 bytes)
    """
    #TODO: We could try to implement another hashing with only 16 bytes to prevent collisions
    # A XOR between both 36 half hashes could also be implemented to try and
    #prevent collisions.

    # Convert the the len of the challenges tables to string and encode to bytes
    count_bytes = str(get_len_challenges()).encode('utf-8')
    
    # Create SHA-256 hash
    hash_obj = hashlib.sha256(count_bytes)
    
    # Get the first 16 bytes of the hash.And return it.
    # NOTE: We perform a digest to obtain the raw bytes

    return hash_obj.digest()[:16]

    

