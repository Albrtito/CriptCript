# TODO: Esta clase se encargará de generar claves y de saber que clave hay que
# usar para descifrar cada mensaje.

# NOTE: Que la clase MessageManger no tome un valor key:srt sino un objeto key
# de esta clase. Ese objeto se obtiene directamente por el mensaje que se queire
# descibrar o se crea al cifrar un mensaje.

#BUG: Esta implementación tiene un problema, si un usuario cambia su contraseña
#(por ahora no pueden) el cifrado de mensajes anteriores se pierde pues ya no se
#puede calcular la clave

#NOTE: Esta clase también ha de asegurar que las claves son de la longitud deseada

import hashlib
from src.mariaDB.query_users import get_user_password
from src.mariaDB.query_challenges import get_len_challenges

def key_from_user(user: str, length = 256) -> str:
    """

    :param user -> String with the username (in hash form)
    :param lenght -> Lenght of the key to generate in BITS
    :return -> Return the value of the key created
    """

    # Get the current password of the user: 
    user_password = get_user_password(user)

    # The user password hash is to big to be an AES key: Get half of it
    len_password = len(user_password)
    half_password = user_password[len_password//2:]

    # Key equals to half the user password 
    key = half_password

    # The key must be 32 bits long so it can later turn into a 256 bit key.
    # Check
    if len(key) == (length//8):
        return key
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

    

