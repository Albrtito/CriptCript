import hashlib
import os

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from src.mariaDB.query_challenges import get_len_challenges
from src.mariaDB.query_users import get_user_password


def key_from_user(hashed_user: str, length=256, salt=None) -> tuple[bytes, bytes]:
    """
    Creates a key derived from the user hashed password.
    :param hashed_user -> String with the username (in hash form)
    :param lenght -> Lenght of the key to generate in BITS
    :return -> Return the value of the key created
    """
    # If the salt is None, generate a new one
    if salt is None:
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
    if type(key) != bytes:
        key = key.encode()

    # The key must be 32 bits long so it can later turn into a 256 bit key.
    # Check
    if len(key) == (length // 8):
        return key, salt
    else:
        raise TypeError("The key doesn't have a valid size")


def new_nonce() -> bytes:
    """
    This function generates a new nonce for AES encription.
    It ensures that this nonce has never been used and has a len of 16 bytes.
    To prevent repeating when the len of the challenges is greater than 16 we can perform a hash.
    :return -> Nonce value (16 bytes)
    """
    # TODO: We could try to implement another hashing with only 16 bytes to prevent collisions
    # A XOR between both 36 half hashes could also be implemented to try and
    # prevent collisions.

    # Convert the the len of the challenges tables to string and encode to bytes
    count_bytes = str(get_len_challenges()).encode("utf-8")

    # Create SHA-256 hash
    hash_obj = hashlib.sha256(count_bytes)

    # Get the first 16 bytes of the hash.And return it.
    # NOTE: We perform a digest to obtain the raw bytes

    return hash_obj.digest()[:16]
