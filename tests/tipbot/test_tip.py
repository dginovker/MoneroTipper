import unittest
import helper
from helper import get_xmr_val

class mainTestCase(unittest.TestCase):

    helper.botname = "MoneroTip"

    def test_parse_tip_amount(self):
        prefix = f"u/{helper.botname} (tip )?"

        self.assertTrue(helper.parse_amount(prefix, f"/u/{helper.botname} 1.0 xmr") == "1.0")
        self.assertTrue(helper.parse_amount(prefix, f"/u/{helper.botname} 1xmr") == "1")
        self.assertTrue(helper.parse_amount(prefix, f"/u/{helper.botname} 5 xmr") == "5")
        self.assertTrue(helper.parse_amount(prefix, f"/u/{helper.botname} tip 1 xmr") == "1")
        self.assertTrue(helper.parse_amount(prefix, f"/u/{helper.botname} tip 1xmr") == "1")

        self.assertTrue(helper.parse_amount(prefix, f"/u/{helper.botname} 1 mxmr") == "0.001")
        self.assertTrue(helper.parse_amount(prefix, f"/u/{helper.botname} 1mxmr") == "0.001")
        self.assertTrue(helper.parse_amount(prefix, f"/u/{helper.botname} tip 1 mxmr") == "0.001")
        self.assertTrue(helper.parse_amount(prefix, f"/u/{helper.botname} tip 1mxmr") == "0.001")

        self.assertTrue(helper.parse_amount(prefix, f"/u/{helper.botname} 1.0$") == str(get_xmr_val(1)))
        self.assertTrue(helper.parse_amount(prefix, f"/u/{helper.botname} $1") == str(get_xmr_val(1)))

        self.assertTrue(helper.parse_amount(prefix, f"Here's some stuff to throw the bot off:\n If you want to peer to peer trade Monero instead of using an exchange, check out LocalMonero: http://localmonero.co/\n/u/{helper.botname} 0.001 XMR") == "0.001")
        self.assertTrue(helper.parse_amount(prefix, f"Thx for finding the bug :) u/{helper.botname} 0.001 XMR") == "0.001")
