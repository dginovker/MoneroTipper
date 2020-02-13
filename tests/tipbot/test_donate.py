import unittest

import helper
from helper import get_xmr_val

class mainTestCase(unittest.TestCase):
    """
    NOTICE: Some of these testcases rely on coingecko's API when calling method_handler.get_xmr_val.
     It is possible that these tests will fail when the value changes during the assert.
    """

    helper.botname = "MoneroTip"

    def test_parse_donate_amount(self):
        self.assertTrue(helper.parse_amount("donate ", "donate 1.0 xmr", 0) == "1.0")
        self.assertTrue(helper.parse_amount("donate ", "donate 1xmr", 0) == "1")

        self.assertTrue(helper.parse_amount("donate ", "donate 1 mxmr", 0) == "0.001")
        self.assertTrue(helper.parse_amount("donate ", "donate 1mxmr", 0) == "0.001")

        self.assertTrue(helper.parse_amount("donate ", "donate 100% of my balance", 1) == "1.0")
        self.assertTrue(helper.parse_amount("donate ", "donate 50% of my balance", 1) == "0.5")
        self.assertTrue(helper.parse_amount("donate ", "donate 0% of my balance", 1) == "0.0")

        self.assertTrue(helper.parse_amount("donate ", "donate 1.0$", 0) == str(get_xmr_val(1)))
        self.assertTrue(helper.parse_amount("donate ", "donate $1", 0) == str(get_xmr_val(1)))
