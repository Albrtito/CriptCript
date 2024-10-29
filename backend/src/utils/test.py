import hashlib
from HashManager import HashManager

def hkdf_expand(passwordHash, length=32, salt=b"", info=b""):
    """
    Given a hash, it expands it. Lenght is considered to be in BYTES 16 bytes = 128bits
    """
    print(passwordHash)
    hashed = HashManager.create_hash(passwordHash)
    print(hashed)
    print(len(hashed))
    
    n = len(hashed)
    halfHashed = hashed[n//2:]
    print(halfHashed)
    print(len(halfHashed))

    hashed_encoded = hashed.encode()
    print(hashed_encoded)
    print(len(hashed_encoded))

    halfHashed_encoded = halfHashed.encode()
    print(halfHashed_encoded)
    print(len(halfHashed_encoded))




    passwordBytes = passwordHash.encode()
    hkdf = hashlib.pbkdf2_hmac("sha256", passwordBytes, salt, 100000, dklen=length)

    print(hkdf)
    print(len(hkdf))
    return hkdf

hkdf_expand("SomePassword")

