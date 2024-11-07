from unittest import TestCase

from src.utils.auth.MACManager import MACManager


class Test_MAC(TestCase):
    """
    Class for testing all MAC implementations
    """

    def test_create_HMAC(self):
        # Creating the HMAC
        key = "12345"
        data = "My data"
        hmac = MACManager.create_HMAC(data, key)
        self.assertEqual(
            hmac,
            b"\xaa\x91\xe5\xfe\xe4c4\x99\xfc6LR\x9eK\xf8\xaa\xce\xc2\x1b\xcb\xd4\x84\xb2\x86\x8a\x1e\xd1\x8cAL?\xa4",
            "Failed on MAC creation",
        )

    def test_verify_HMAC_TRUE(self):
        # Creating the MAC
        key = "12345"
        data = "My data"
        hmac = MACManager.create_HMAC(data, key)

        # Verifyint the HMAC
        key2 = "12345"
        data2 = "My data"
        output = MACManager.verify_HMAC(key2, data2, hmac)

        self.assertEqual(
            output, True, "Test for a verification with positive output(True)"
        )

    def test_verify_HMAC_DataDiff(self):
        # Creating the MAC
        key = "12345"
        data = "My data"
        hmac = MACManager.create_HMAC(data, key)

        # Verifyint the HMAC
        key2 = "12345"
        data2 = "Different Data"

        with self.assertRaises(ValueError):
            MACManager.verify_HMAC(key2, data2, hmac)

    def test_verify_HMAC_KeyDiff(self):
        # Creating the MAC
        key = "54321"
        data = "My data"
        hmac = MACManager.create_HMAC(data, key)

        # Verifyint the HMAC
        key2 = "12345"
        data2 = "My data"

        with self.assertRaises(ValueError):
            MACManager.verify_HMAC(key2, data2, hmac)

    def test_verify_HMAC_HMACDiff(self):
        # Creating the MAC
        key = "12345"
        data = "My data"
        hmac = MACManager.create_HMAC(data, key)

        # Creating second HMAC
        key3 = "My data"
        data3 = "12345"
        hmac2 = MACManager.create_HMAC(data3, key3)

        # Verifyint the HMAC
        key2 = "12345"
        data2 = "My data"

        with self.assertRaises(ValueError):
            print(MACManager.verify_HMAC(key2, data2, hmac2))
