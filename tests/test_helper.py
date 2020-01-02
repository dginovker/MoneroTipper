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

    helper.botname = "MoneroTip"

    def test_get_local_wallet_address(self):
        print(helper.get_local_wallet_address("osrsneedsf2p"))
