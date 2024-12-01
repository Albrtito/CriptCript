from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.hashes import SHA256
from datetime import datetime, timezone, timedelta

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
        private_key = private_key

        public_key = public_key

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
    def sign_certificate(certificate: x509.CertificateBuilder, private_key: rsa.RSAPrivateKey) -> x509.Certificate:
        """
        Firma un certificado X.509 con la clave privada proporcionada.

        Args:
            certificate (x509.CertificateBuilder): Certificado sin firmar.
            private_key (rsa.RSAPrivateKey): Clave privada para firmar el certificado.

        Returns:
            x509.Certificate: Certificado X.509 firmado.
        """
        signed_certificate = certificate.sign(private_key, SHA256())
        return signed_certificate