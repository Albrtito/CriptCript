""" 
    This module is responsible for managing the creation, deletion, edition and user login.
"""

import logging

from flask import Blueprint, Flask, jsonify, make_response, request
from src.mariaDB.query_certificates import get_certificates
from src.mariaDB.query_challenges import (insert_challenge, return_all_public,
                                          return_shared_with_user)
from src.mariaDB.query_digital_firm import (get_private_ciphered_key,
                                            get_public_key, get_signature,
                                            insert_signature_in_db)
from src.mariaDB.query_keys import get_salt_from_db, insert_salt_in_db
from src.utils.certificate.CertificateManager import CertificateManager
from src.utils.digitalSign.DigitalSignManager import (create_signature,
                                                      verify_signature)
from src.utils.HashManager import HashManager
from src.utils.keys import KeyGen
from src.utils.MessageManager import MessageManager

logging.basicConfig(level=logging.DEBUG)

challenges_bp = Blueprint("challenges", __name__)


@challenges_bp.route("/create_challenge", methods=["POST"])
def create_challenge():
    """
    Creates a new challenge in the database
    Return: returns a response object
    """
    data = request.get_json()
    title = data.get("title")
    document = data.get("document")
    userToShare = data.get("userToShare")
    userLogged = data.get("userLogged")

    # Check that there is a logged user
    if len(userLogged) == 0:
        response = make_response(jsonify({"response": "There is no user logged"}), 422)
        return response
    else:
        # Hash the value of the user to obtain the reference in the db
        hashedUser = HashManager.create_hash(userLogged)

        # ENCRIPTION
        # Get user hash and the key from KeyGen class
        key, salt = KeyGen.key_from_user(hashedUser)
        # Cipher the title and the document
        cipheredTitle = MessageManager.cipher_message(title, key)
        cipheredMessage = MessageManager.cipher_message(document, key)

        # AUTHENTICATION
        auth = MessageManager.auth_create(cipheredTitle + cipheredMessage, key)

        # SIGNATURE
        private_ciphered_key = get_private_ciphered_key(hashedUser)
        # Debugging
        logging.debug("%s", private_ciphered_key)
        logging.debug("Type of private key %s", type(private_ciphered_key))
        # Ge the salt referenced to the private key
        signed_salt = get_salt_from_db(private_ciphered_key)
        sign_key, signed_salt = KeyGen.key_from_user(hashedUser, 256, signed_salt)
        private_key = MessageManager.decipher_message(private_ciphered_key, sign_key)
        logging.debug(
            "create_challenge() --- Deciphered private key %s, type %s",
            private_key,
            type(private_key),
        )  # type is string
        signature = create_signature(private_key, cipheredMessage)
        logging.debug(
            "create_signature() --- Signature %s, type of signature %s",
            signature,
            type(signature),
        )  # type is bytes

    # SAVING:
    # Insert the ciphered challenge into the db.
    if len(userToShare) == 0:
        insert_challenge(cipheredTitle, hashedUser, cipheredMessage, False, auth)
    else:
        userToShareHash = HashManager.create_hash(userToShare)
        insert_challenge(
            cipheredTitle, hashedUser, cipheredMessage, True, auth, userToShareHash
        )

    # Insert the signature into the db
    insert_signature_in_db(cipheredMessage, signature)
    # Insert the salt into the db
    insert_salt_in_db(cipheredMessage, salt)

    # Return a response
    response = make_response(jsonify({"response": "Challenge has been created!"}), 201)
    return response


@challenges_bp.route("/get_public_challenges", methods=["GET"])
def get_public_challenges():
    """
    Returns a response with all public challenges available for the user
    """
    publicChallenges = return_all_public()
    if not publicChallenges:
        response = make_response(jsonify({"response": "No public challenges"}), 201)
        return response

    response = []
    # fields to decipher: title = 1, content = 2, author = 3, where numbers = index in the array
    for i in range(0, len(publicChallenges), 1):  # iterate through every row
        cipheredTitle = publicChallenges[i][1]
        hashedAuthor = publicChallenges[i][2]
        cipheredContent = publicChallenges[i][3]
        auth_value = publicChallenges[i][4]

        # KEY GENERATION FOR AUTH AND DECIPHER
        challenge_salt = get_salt_from_db(cipheredContent)
        key, _ = KeyGen.key_from_user(hashedAuthor, salt=challenge_salt)

        # AUTHENTICATION
        if not MessageManager.auth_verify(
            auth_value, cipheredTitle + cipheredContent, key
        ):
            raise Exception("The message is not authenticated")

        # SIGNATURE
        # Get key and certificate of the author of the challenge
        public_key = get_public_key(hashedAuthor)
        certificate = get_certificates(hashedAuthor)
        logging.debug("Certificate obtain %s, \n\n %s", type(certificate), certificate)
        private_ciphered_key_cert = certificate[2]
        certificate = certificate[3]

        sign_salt = get_salt_from_db(private_ciphered_key_cert)
        hashedAuthorKey, _ = KeyGen.key_from_user(hashedAuthor, 256, sign_salt)
        private_key_cert = MessageManager.decipher_message(
            private_ciphered_key_cert, hashedAuthorKey
        )
        logging.debug(
            "Private key from the certificate %s, \n\n %s \n",
            type(certificate),
            certificate,
        )

        if not CertificateManager.verify_certificate(
            private_key_cert.encode(), public_key.encode(), certificate
        ):
            logging.debug("The message %s was not certified... Woopsie", i)
            publicChallenges.pop(i)

        logging.debug("public key: %s and its type %s", public_key, type(public_key))
        # recover the signature from the message
        signature = get_signature(cipheredContent)
        logging.debug("signature: %s and its type %s", signature, type(signature))
        # check the signature
        if not verify_signature(public_key, cipheredContent, signature):
            logging.debug(
                "The message %s has a problem with its signature... It will not be shown",
                i,
            )
            publicChallenges.pop(i)
        else:
            # DECIPHER:
            title = MessageManager.decipher_message(cipheredTitle, key)
            content = MessageManager.decipher_message(cipheredContent, key)

            json = {"title": title, "content": content}
            response.append(json)

    response = make_response(jsonify({"response": response}), 201)
    return response


@challenges_bp.route("/get_private_challenges", methods=["GET"])
def get_private_challenges():
    """
    Returns a response with all the private challenges shared with an user
    """
    user = request.args.get("user")

    user_hash = HashManager.create_hash(user)
    privateChallenges = return_shared_with_user(user_hash)
    response = []
    if not privateChallenges:
        response = make_response(jsonify({"response": "No private challenges"}), 201)
        return response

    for i in range(0, len(privateChallenges), 1):

        cipheredTitle = privateChallenges[i][1]
        hashedAuthor = privateChallenges[i][2]
        cipheredContent = privateChallenges[i][3]
        auth_value = privateChallenges[i][4]

        # Get user hash and key from KeyGen class
        challenge_salt = get_salt_from_db(cipheredContent)
        key, challenge_salt = KeyGen.key_from_user(hashedAuthor, salt=challenge_salt)

        # Check authentication of the message:
        if not MessageManager.auth_verify(
            auth_value, cipheredTitle + cipheredContent, key
        ):
            # TODO: Cambiar la response y hacer que se modifique en el frontend
            raise Exception("The message is not authenticated")
        # recover the public key of the user
        public_key = get_public_key(hashedAuthor)
        certificate = get_certificates(hashedAuthor)
        logging.debug("Certificate obtain %s, \n\n %s", type(certificate), certificate)

        private_ciphered_key_cert = certificate[2]
        certificate = certificate[3]
        cert_salt = get_salt_from_db(private_ciphered_key_cert)
        hashedAuthorKey, cert_salt = KeyGen.key_from_user(hashedAuthor, salt=cert_salt)
        private_key_cert = MessageManager.decipher_message(
            private_ciphered_key_cert, hashedAuthorKey
        )
        logging.debug(
            "Private key from the certificate %s, \n\n %s \n",
            type(certificate),
            certificate,
        )

        if not CertificateManager.verify_certificate(
            private_key_cert.encode(), public_key.encode(), certificate
        ):
            logging.debug("The message %s was not certified... Woopsie", i)
            privateChallenges.pop(i)

        logging.debug("public key: %s and its type %s", public_key, type(public_key))
        # recover the signature from the message
        signature = get_signature(cipheredContent)
        logging.debug("signature: %s and its type %s", signature, type(signature))
        # check the signature
        logging.debug("Procedding into signature verification")
        if not verify_signature(public_key, cipheredContent, signature):
            logging.warning(
                "The message %s has a problem with its signature... It will not be shown",
                i,
            )
            privateChallenges.pop(i)
        else:
            # Decipher the title and content
            title = MessageManager.decipher_message(cipheredTitle, key)
            content = MessageManager.decipher_message(cipheredContent, key)

            json = {"title": title, "content": content}
            response.append(json)

    response = make_response(jsonify({"response": response}))
    return response
