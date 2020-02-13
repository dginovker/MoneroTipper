import unittest

import helper

class mainTestCase(unittest.TestCase):
    """
    NOTICE: Some of these testcases rely on coingecko's API when calling method_handler.get_xmr_val.
     It is possible that these tests will fail when the value changes during the assert.
    """

    helper.botname = "MoneroTip"

    def test_parse_withdrawal_amount(self):

        self.assertTrue(helper.parse_amount("withdraw ", "withdraw 1xmr") == "1")
        self.assertTrue(helper.parse_amount("withdraw ", "withdraw 1.0 xmr") == "1.0")

        self.assertTrue(helper.parse_amount("withdraw ", "withdraw 1 mxmr") == "0.001")
        self.assertTrue(helper.parse_amount("withdraw ", "withdraw 1mxmr") == "0.001")

        self.assertTrue(helper.parse_amount("withdraw ", "withdraw 1.0$") == str(helper.get_xmr_val(1)))
        self.assertTrue(helper.parse_amount("withdraw ", "withdraw $1") == str(helper.get_xmr_val(1)))
