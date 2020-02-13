import unittest

import helper
from tipbot.anon_tip import parse_anon_tip_amount, parse_anon_tip_recipient
from helper import get_xmr_val

class mainTestCase(unittest.TestCase):
    """
    NOTICE: Some of these testcases rely on coingecko's API when calling method_handler.get_xmr_val.
     It is possible that these tests will fail when the value changes during the assert.
    """

    helper.botname = "MoneroTip"

    def test_parse_anontip_amount(self):
        self.assertTrue(helper.parse_amount(f"anonymous tip {helper.botname} ", f"anonymous tip {helper.botname} 1 xmr") == "1")
        self.assertTrue(helper.parse_amount(f"anonymous tip {helper.botname} ", f"anonymous tip {helper.botname} 1xmr") == "1")
        self.assertTrue(helper.parse_amount(f"anonymous tip {helper.botname} ", f"anonymous tip {helper.botname} 1 mxmr") == "0.001")
        self.assertTrue(helper.parse_amount(f"anonymous tip {helper.botname} ", f"anonymous tip {helper.botname} 1mxmr") == "0.001")

        self.assertTrue(helper.parse_amount(f"anonymous tip {helper.botname} ", f"anonymous tip {helper.botname} 1$") == str(get_xmr_val(1)))
        self.assertTrue(helper.parse_amount(f"anonymous tip {helper.botname} ", f"anonymous tip {helper.botname} $1.0") == str(get_xmr_val(1)))

    def test_parse_anon_tip_recipient(self):
        self.assertTrue(parse_anon_tip_recipient(f"anonymous tip big .1 mxmr") == "big")
        self.assertTrue(parse_anon_tip_recipient(f"anonymous tip big      .1 mxmr") == "big")
        self.assertTrue(parse_anon_tip_recipient(f"Anonymous tip OsrsNeedsF2P $5") == "osrsneedsf2p")
