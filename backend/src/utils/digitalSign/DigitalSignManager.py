#NOTE: esta clase tiene todos los métodos que se utulizarán para la Firma Digital, incluso uno que genera clases. En ../keys ya existe un archivo que maneje todo esto; pero solo si le pasamos un usuario. Para este caso, ya que la arquitectura de la firma cambia totalmente (en la ddbb), se crea este nuevo archivo.

#TODO: futuro refactor solo si es posible. Ver tras el push del Fernet de Alberto

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

# Función para generar el par de claves RSA
def generate_rsa_keys():
    """
    Invoca a esta función para generar un par de claves RSA para Firma Digital
    """
    # Generar la clave privada
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # Generar la clave pública
    public_key = private_key.public_key()

    # Serializar la clave privada en formato PEM
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Serializar la clave pública en formato PEM
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_pem.decode(), public_pem.decode()