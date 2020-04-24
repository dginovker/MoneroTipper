import unittest

import helper

class mainTestCase(unittest.TestCase):

    def test_switching_ports_to_testnet(self):
        self.assertTrue(helper.ports.monerod_port == 18081)
        helper.ports.ports_to_testnet()
        self.assertTrue(helper.ports.monerod_port == 28081)

    def test_get_xmr_val(self):
        self.assertTrue(float(helper.get_xmr_val(5)) > 0)
        self.assertTrue(float(helper.get_xmr_val(1)) < 5000)

    def test_get_dollar_val(self):
        self.assertTrue(float(helper.get_dollar_val(1)) > 0)
        self.assertTrue(float(helper.get_dollar_val(1)) < 5000)

        self.assertTrue(helper.get_dollar_val(helper.get_xmr_val(5)) == "5.00")

    def test_parse_amount(self):
        self.assertTrue(helper.parse_amount("donate ", "donate 5 xmr", 2) == "5")
        self.assertTrue(helper.parse_amount("donate ", "donate 5$", 2) == helper.get_xmr_val(5))
        self.assertTrue(float(helper.parse_amount("donate ", "donate 50% of my balance", 2)) == float(1))

    def test_istxid(self):
        self.assertTrue(helper.is_txid("7a4a8a94d6f0aebe825a298bf682d9abba5532c4057f735794900731d3ab3de8"))
        self.assertFalse(helper.is_txid("Anything else"))

    def test_format_decimial(self):
        self.assertTrue(helper.format_decimal(1.2345, 4) == "1.2345")
        self.assertTrue(helper.format_decimal(1.7898, 3) == "1.790")
        self.assertTrue(helper.format_decimal(1.7898, 0) == "2")
