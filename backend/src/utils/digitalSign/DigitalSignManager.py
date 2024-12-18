#NOTE: esta clase tiene todos los métodos que se utulizarán para la Firma Digital, incluso uno que genera clases. En ../keys ya existe un archivo que maneje todo esto; pero solo si le pasamos un usuario. Para este caso, ya que la arquitectura de la firma cambia totalmente (en la ddbb), se crea este nuevo archivo.

#TODO: futuro refactor solo si es posible. Ver tras el push del Fernet de Alberto

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key

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

def create_signature(private_key_pem, message):
    """
    Crea una firma digital para un mensaje usando una clave privada RSA.

    Args:
        private_key_pem (string): Clave privada en formato PEM.
        message (bytes): Mensaje que será firmado.

    Returns:
        bytes: La firma digital generada.
    """
    # Cargar la clave privada desde el formato PEM
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode(),
        password=None,  # Sin contraseña
        backend=default_backend()
    )

    # Crear la firma digital
    signature = private_key.sign(
        message, 
        padding.PKCS1v15(),  # Esquema de padding
        hashes.SHA256()  # Algoritmo de hash
    )

    return signature

def verify_signature(public_key_pem: str, message: bytes, signature: bytes) -> bool:
    """
    Verifica una firma digital utilizando la clave pública.

    Args:
        public_key_pem (str): Clave pública en formato PEM como cadena.
        message (str): Mensaje original.
        signature (bytes): Firma digital en formato bytes.

    Returns:
        bool: True si la firma es válida, False si no lo es.
    """
    try:
        # Convertir la clave pública de PEM (cadena) a un objeto usable
        public_key = load_pem_public_key(public_key_pem.encode())

        # Verificar la firma
        public_key.verify(
            signature,
            message,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True  # La firma es válida
    except Exception as e:
        print(f"Error al verificar la firma: {e}")
        return False  # La firma no es válida