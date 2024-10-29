# TODO: Esta clase se encargará de generar claves y de saber que clave hay que
# usar para descifrar cada mensaje.

# NOTE: Que la clase MessageManger no tome un valor key:srt sino un objeto key
# de esta clase. Ese objeto se obtiene directamente por el mensaje que se queire
# descibrar o se crea al cifrar un mensaje.

#BUG: Esta implementación tiene un problema, si un usuario cambia su contraseña
#(por ahora no pueden) el cifrado de mensajes anteriores se pierde pues ya no se
#puede calcular la clave

#NOTE: Esta clase también ha de asegurar que las claves son de la longitud deseada

from src.mariaDB.query_users import get_user_password

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


