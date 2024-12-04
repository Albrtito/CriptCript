from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.hashes import SHA256
from datetime import datetime, timezone, timedelta
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.primitives.asymmetric import padding


class CertificateManager():
    """
    This class implements everything related with certificates (and its entities) for a detailed verification of the public key
    """
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def generate_x509_certificate(
        common_name: str,
        public_key: bytes,
        private_key: bytes,
        country_name: str = "ES",
        state_name: str = "Madrid",
        locality_name: str = "Leganés",
        organization_name: str = "UC3M",
        valid_days: int = 365,
    ):
        """
        Genera un certificado X.509 autofirmado junto con su clave privada.

        Args:
            common_name (str): Nombre común del sujeto/emisor.
            public_key (bytes): clave pública usada en la firma
            private_key (bytes): clave privada (sin cifrar) usada en la firma
            country_name (str): Nombre del país (ISO 3166-1). Default: "ES".
            state_name (str): Nombre del estado/provincia. Default: "Madrid".
            locality_name (str): Nombre de la localidad. Default: "Leganés".
            organization_name (str): Nombre de la organización. Default: "UC3M".
            valid_days (int): Días de validez del certificado. Default: 365.

        Returns:
            dict: Diccionario con 'certificate_pem' y 'private_key_pem' en formato PEM.
        """
        private_key = serialization.load_pem_private_key(private_key, password=None, backend=default_backend())

        public_key = serialization.load_pem_public_key(public_key, backend=default_backend()) # necesitamos cargar de bytes a un objeto RSAKey

        # Crear sujeto y emisor
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, country_name),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state_name),
            x509.NameAttribute(NameOID.LOCALITY_NAME, locality_name),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization_name),
            x509.NameAttribute(NameOID.COMMON_NAME, common_name),
        ])

        # Crear certificado
        certificate = x509.CertificateBuilder()\
            .subject_name(subject)\
            .issuer_name(issuer)\
            .public_key(public_key)\
            .serial_number(x509.random_serial_number())\
            .not_valid_before(datetime.now(timezone.utc))\
            .not_valid_after(datetime.now(timezone.utc) + timedelta(days=valid_days))\
            .add_extension(
                x509.SubjectAlternativeName([x509.DNSName(common_name)]),
                critical=False,
            )\
            .sign(private_key, SHA256())

        # Exportar el certificado y la clave privada
        certificate_pem = certificate.public_bytes(serialization.Encoding.PEM)
        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

        return {
            "certificate_pem": certificate_pem,
            "private_key_pem": private_key_pem # usada para firmar el certificado
        }
    
    @staticmethod
    def generate_x509_certificate_for_another_entity(
        issuer_private_key: bytes,
        issuer_name: str,
        subject_name: str,
        subject_public_key: bytes,
        country_name: str = "ES",
        state_name: str = "Madrid",
        locality_name: str = "Leganés",
        organization_name: str = "UC3M",
        valid_days: int = 365,
    ):
        """
        Genera un certificado X.509 para una entidad (subject) firmado por otra entidad (issuer).

        Args:
            issuer_private_key (bytes): Clave privada del emisor (firma).
            issuer_name (str): Nombre común del emisor.
            subject_name (str): Nombre común del sujeto.
            subject_public_key (bytes): Clave pública del sujeto.
            country_name (str): Nombre del país (ISO 3166-1). Default: "ES".
            state_name (str): Nombre del estado/provincia. Default: "Madrid".
            locality_name (str): Nombre de la localidad. Default: "Leganés".
            organization_name (str): Nombre de la organización. Default: "UC3M".
            valid_days (int): Días de validez del certificado. Default: 365.

        Returns:
            dict: Diccionario con 'certificate_pem' en formato PEM.
        """
        # Cargar las claves del emisor y el sujeto
        issuer_private_key = serialization.load_pem_private_key(issuer_private_key, password=None, backend=default_backend())
        subject_public_key = serialization.load_pem_public_key(subject_public_key, backend=default_backend())

        # Crear el nombre del emisor y del sujeto
        issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, country_name),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state_name),
            x509.NameAttribute(NameOID.LOCALITY_NAME, locality_name),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization_name),
            x509.NameAttribute(NameOID.COMMON_NAME, issuer_name),
        ])
        subject = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, country_name),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state_name),
            x509.NameAttribute(NameOID.LOCALITY_NAME, locality_name),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization_name),
            x509.NameAttribute(NameOID.COMMON_NAME, subject_name),
        ])

        # Crear el certificado
        certificate = x509.CertificateBuilder()\
            .subject_name(subject)\
            .issuer_name(issuer)\
            .public_key(subject_public_key)\
            .serial_number(x509.random_serial_number())\
            .not_valid_before(datetime.now(timezone.utc))\
            .not_valid_after(datetime.now(timezone.utc) + timedelta(days=valid_days))\
            .add_extension(
                x509.SubjectAlternativeName([x509.DNSName(subject_name)]),
                critical=False,
            )\
            .sign(issuer_private_key, SHA256())

        # Exportar el certificado
        certificate_pem = certificate.public_bytes(serialization.Encoding.PEM)

        return {
            "certificate_pem": certificate_pem,
        }

    
    @staticmethod
    def verify_certificate(private_key: bytes, public_key: bytes, certificate_pem: bytes) -> bool:
        """
        Verifica si el certificado es válido usando la clave privada y la clave pública proporcionadas.

        Args:
            private_key (rsa.RSAPrivateKey): Clave privada asociada al certificado.
            public_key (rsa.RSAPublicKey): Clave pública asociada al certificado.
            certificate_pem (bytes): Certificado X.509 en formato PEM.

        Returns:
            bool: True si el certificado es válido, False en caso contrario.
        """
        # Cargar el certificado desde el formato PEM
        certificate = load_pem_x509_certificate(certificate_pem)
        private_key = serialization.load_pem_private_key(private_key, password=None, backend=default_backend())
        public_key = serialization.load_pem_public_key(public_key, backend=default_backend()) # necesitamos cargar de bytes a un objeto RSAKey


        # Obtener la clave pública del certificado
        certificate_public_key = certificate.public_key()

        # Crear un mensaje de prueba para validar la relación entre claves
        message = b"test_message_for_certificate_validation"

        try:
            # Firmar el mensaje con la clave privada
            signature = private_key.sign(
                message,
                padding.PKCS1v15(),
                SHA256()
            )

            # Verificar la firma con la clave pública del certificado
            certificate_public_key.verify(
                signature,
                message,
                padding.PKCS1v15(),
                SHA256()
            )

            # Verificar si la clave pública proporcionada coincide con la clave pública del certificado
            if public_key.public_numbers() == certificate_public_key.public_numbers():
                return True

        except Exception as e:
            # Si algo falla, el certificado no es válido
            print(f"Error al verificar el certificado: {e}")

        return False
