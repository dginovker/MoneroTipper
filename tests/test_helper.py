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
