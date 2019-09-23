import unittest
try:
    from unittest.mock import patch, Mock, MagicMock
except ImportError:
    from mock import patch, Mock
import helper


class mainTestCase(unittest.TestCase):

    def test_switching_ports_to_testnet(self):
        self.assertTrue(helper.ports.monerod_port == 18081)
        helper.ports.ports_to_testnet()
        self.assertTrue(helper.ports.monerod_port == 28081)

