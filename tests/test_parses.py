import unittest

import helper
from tipbot.anon_tip import parse_anon_tip_amount
from helper import get_xmr_val
from tipbot.donate import parse_donate_amount
from tipbot.tip import parse_tip_amount
from tipbot.withdraw import parse_withdrawl_amount

try:
    from unittest.mock import patch, Mock, MagicMock
except ImportError:
    from mock import patch, Mock

class mainTestCase(unittest.TestCase):
    """
    NOTICE: Some of these testcases rely on coingecko's API when calling method_handler.get_xmr_val.
     It is possible that these tests will fail when the value changes during the assert.
    """

    helper.botname = "MoneroTip"

    def test_parse_tip_amount(self):
        self.assertTrue(
            parse_tip_amount(f"/u/{helper.botname} 1.0 xmr", helper.botname) == "1.0")
        self.assertTrue(parse_tip_amount(f"/u/{helper.botname} 1xmr", helper.botname) == "1")
        self.assertTrue(
            parse_tip_amount(f"/u/{helper.botname} tip 1 xmr", helper.botname) == "1")
        self.assertTrue(
            parse_tip_amount(f"/u/{helper.botname} tip 1xmr", helper.botname) == "1")

        self.assertTrue(
            parse_tip_amount(f"/u/{helper.botname} 1 mxmr", helper.botname) == "0.001")
        self.assertTrue(
            parse_tip_amount(f"/u/{helper.botname} 1mxmr", helper.botname) == "0.001")
        self.assertTrue(
            parse_tip_amount(f"/u/{helper.botname} tip 1 mxmr", helper.botname) == "0.001")
        self.assertTrue(
            parse_tip_amount(f"/u/{helper.botname} tip 1mxmr", helper.botname) == "0.001")

        self.assertTrue(parse_tip_amount(f"/u/{helper.botname} 1.0$", helper.botname) == str(
            get_xmr_val(1)))
        self.assertTrue(parse_tip_amount(f"/u/{helper.botname} $1", helper.botname) == str(
            get_xmr_val(1)))

    def test_parse_withdrawal_amount(self):
        self.assertTrue(parse_withdrawl_amount("withdraw 1.0 xmr") == "1.0")
        self.assertTrue(parse_withdrawl_amount("withdraw 1xmr") == "1")

        self.assertTrue(parse_withdrawl_amount("withdraw 1 mxmr") == "0.001")
        self.assertTrue(parse_withdrawl_amount("withdraw 1mxmr") == "0.001")

        self.assertTrue(parse_withdrawl_amount("withdraw 1.0$") == str(get_xmr_val(1)))
        self.assertTrue(parse_withdrawl_amount("withdraw $1") == str(get_xmr_val(1)))

    def test_parse_donate_amount(self):
        self.assertTrue(parse_donate_amount("donate 1.0 xmr", 0) == "1.0")
        self.assertTrue(parse_donate_amount("donate 1xmr", 0) == "1")

        self.assertTrue(parse_donate_amount("donate 1 mxmr", 0) == "0.001")
        self.assertTrue(parse_donate_amount("donate 1mxmr", 0) == "0.001")

        self.assertTrue(parse_donate_amount("donate 100% of my balance", 1) == "1.0")
        self.assertTrue(parse_donate_amount("donate 50% of my balance", 1) == "0.5")
        self.assertTrue(parse_donate_amount("donate 0% of my balance", 1) == "0.0")

        self.assertTrue(parse_donate_amount("donate 1.0$", 0) == str(get_xmr_val(1)))
        self.assertTrue(parse_donate_amount("donate $1", 0) == str(get_xmr_val(1)))

    def test_parse_anontip_amount(self):
        self.assertTrue(parse_anon_tip_amount(f"anonymous tip {helper.botname} 1 xmr") == "1")
        self.assertTrue(parse_anon_tip_amount(f"anonymous tip {helper.botname} 1xmr") == "1")
        self.assertTrue(parse_anon_tip_amount(f"anonymous tip {helper.botname} 1 mxmr") == "0.001")
        self.assertTrue(parse_anon_tip_amount(f"anonymous tip {helper.botname} 1mxmr") == "0.001")

        self.assertTrue(parse_anon_tip_amount(f"anonymous tip {helper.botname} 1$") == str(
            get_xmr_val(1)))
        self.assertTrue(parse_anon_tip_amount(f"anonymous tip {helper.botname} $1.0") == str(
            get_xmr_val(1)))
