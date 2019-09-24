import unittest
from tipperInteractions.comment_parse import MethodHandler

try:
    from unittest.mock import patch, Mock, MagicMock
except ImportError:
    from mock import patch, Mock

class mainTestCase(unittest.TestCase):
    """
    NOTICE: Some of these testcases rely on coingecko's API when calling method_handler.get_xmr_val.
     It is possible that these tests will fail when the value changes during the assert.
    """

    method_handler = MethodHandler(None, botname="monerotip")

    def test_parse_tip_amount(self):
        self.assertTrue(self.method_handler.parse_tip_amount("/u/monerotip 1.0 xmr") == "1.0")
        self.assertTrue(self.method_handler.parse_tip_amount("/u/monerotip 1xmr") == "1")
        self.assertTrue(self.method_handler.parse_tip_amount("/u/monerotip tip 1 xmr") == "1")
        self.assertTrue(self.method_handler.parse_tip_amount("/u/monerotip tip 1xmr") == "1")

        self.assertTrue(self.method_handler.parse_tip_amount("/u/monerotip 1 mxmr") == "0.001")
        self.assertTrue(self.method_handler.parse_tip_amount("/u/monerotip 1mxmr") == "0.001")
        self.assertTrue(self.method_handler.parse_tip_amount("/u/monerotip tip 1 mxmr") == "0.001")
        self.assertTrue(self.method_handler.parse_tip_amount("/u/monerotip tip 1mxmr") == "0.001")

        self.assertTrue(self.method_handler.parse_tip_amount("/u/monerotip 1.0$") == str(self.method_handler.get_xmr_val(1)))
        self.assertTrue(self.method_handler.parse_tip_amount("/u/monerotip $1") == str(self.method_handler.get_xmr_val(1)))

    def test_parse_withdrawal_amount(self):
        self.assertTrue(self.method_handler.parse_withdrawl_amount("withdraw 1.0 xmr") == "1.0")
        self.assertTrue(self.method_handler.parse_withdrawl_amount("withdraw 1xmr") == "1")

        self.assertTrue(self.method_handler.parse_withdrawl_amount("withdraw 1 mxmr") == "0.001")
        self.assertTrue(self.method_handler.parse_withdrawl_amount("withdraw 1mxmr") == "0.001")

        self.assertTrue(self.method_handler.parse_withdrawl_amount("withdraw 1.0$") == str(self.method_handler.get_xmr_val(1)))
        self.assertTrue(self.method_handler.parse_withdrawl_amount("withdraw $1") == str(self.method_handler.get_xmr_val(1)))

    def test_parse_donate_amount(self):
        self.assertTrue(self.method_handler.parse_donate_amount("donate 1.0 xmr", 0) == "1.0")
        self.assertTrue(self.method_handler.parse_donate_amount("donate 1xmr", 0) == "1")

        self.assertTrue(self.method_handler.parse_donate_amount("donate 1 mxmr", 0) == "0.001")
        self.assertTrue(self.method_handler.parse_donate_amount("donate 1mxmr", 0) == "0.001")

        self.assertTrue(self.method_handler.parse_donate_amount("donate 100% of my balance", 1) == "1.0")
        self.assertTrue(self.method_handler.parse_donate_amount("donate 50% of my balance", 1) == "0.5")
        self.assertTrue(self.method_handler.parse_donate_amount("donate 0% of my balance", 1) == "0.0")

        self.assertTrue(self.method_handler.parse_donate_amount("donate 1.0$", 0) == str(self.method_handler.get_xmr_val(1)))
        self.assertTrue(self.method_handler.parse_donate_amount("donate $1", 0) == str(self.method_handler.get_xmr_val(1)))

    def test_parse_anontip_amount(self):
        self.assertTrue(self.method_handler.parse_anontip_amount("anonymous tip monerotipsbot 1 xmr") == "1")
        self.assertTrue(self.method_handler.parse_anontip_amount("anonymous tip monerotipsbot 1xmr") == "1")
        self.assertTrue(self.method_handler.parse_anontip_amount("anonymous tip monerotipsbot 1 mxmr") == "0.001")
        self.assertTrue(self.method_handler.parse_anontip_amount("anonymous tip monerotipsbot 1mxmr") == "0.001")

        self.assertTrue(self.method_handler.parse_anontip_amount("anonymous tip monerotipsbot 1$") == str(self.method_handler.get_xmr_val(1)))
        self.assertTrue(self.method_handler.parse_anontip_amount("anonymous tip monerotipsbot $1.0") == str(self.method_handler.get_xmr_val(1)))
