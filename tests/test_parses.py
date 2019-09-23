import unittest
from tipperInteractions.comment_parse import MethodHandler

try:
    from unittest.mock import patch, Mock, MagicMock
except ImportError:
    from mock import patch, Mock

class mainTestCase(unittest.TestCase):

    method_handler = MethodHandler(None)

    def test_parse_tip_amount(self):
        self.assertTrue(self.method_handler.parse_tip_amount("/u/monerotipsbot 1.0 xmr") == "1.0")
        self.assertTrue(self.method_handler.parse_tip_amount("/u/monerotipsbot 1xmr") == "1")
        self.assertTrue(self.method_handler.parse_tip_amount("/u/monerotipsbot tip 1 xmr") == "1")
        self.assertTrue(self.method_handler.parse_tip_amount("/u/monerotipsbot tip 1xmr") == "1")

        self.assertTrue(self.method_handler.parse_tip_amount("/u/monerotipsbot 1 mxmr") == "0.001")
        self.assertTrue(self.method_handler.parse_tip_amount("/u/monerotipsbot 1mxmr") == "0.001")
        self.assertTrue(self.method_handler.parse_tip_amount("/u/monerotipsbot tip 1 mxmr") == "0.001")
        self.assertTrue(self.method_handler.parse_tip_amount("/u/monerotipsbot tip 1mxmr") == "0.001")

    def test_parse_withdrawal_amount(self):
        self.assertTrue(self.method_handler.parse_withdrawl_amount("withdraw 1.0 xmr") == "1.0")
        self.assertTrue(self.method_handler.parse_withdrawl_amount("withdraw 1xmr") == "1")

        self.assertTrue(self.method_handler.parse_withdrawl_amount("withdraw 1 mxmr") == "0.001")
        self.assertTrue(self.method_handler.parse_withdrawl_amount("withdraw 1mxmr") == "0.001")

    def test_parse_donate_amount(self):
        self.assertTrue(self.method_handler.parse_donate_amount("donate 1.0 xmr", 1) == "1.0")
        self.assertTrue(self.method_handler.parse_donate_amount("donate 1xmr", 1) == "1")

        self.assertTrue(self.method_handler.parse_donate_amount("donate 1 mxmr", 1) == "0.001")
        self.assertTrue(self.method_handler.parse_donate_amount("donate 1mxmr", 1) == "0.001")

        self.assertTrue(self.method_handler.parse_donate_amount("donate 100% of my balance", 1) == "1.0")
        self.assertTrue(self.method_handler.parse_donate_amount("donate 50% of my balance", 1) == "0.5")
        self.assertTrue(self.method_handler.parse_donate_amount("donate 0% of my balance", 1) == "0.0")
