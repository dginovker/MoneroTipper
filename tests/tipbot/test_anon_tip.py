import unittest

import helper
from tipbot.anon_tip import parse_anon_tip_amount
from helper import get_xmr_val

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

    def test_parse_anontip_amount(self):
        self.assertTrue(parse_anon_tip_amount(f"anonymous tip {helper.botname} 1 xmr") == "1")
        self.assertTrue(parse_anon_tip_amount(f"anonymous tip {helper.botname} 1xmr") == "1")
        self.assertTrue(parse_anon_tip_amount(f"anonymous tip {helper.botname} 1 mxmr") == "0.001")
        self.assertTrue(parse_anon_tip_amount(f"anonymous tip {helper.botname} 1mxmr") == "0.001")

        self.assertTrue(parse_anon_tip_amount(f"anonymous tip {helper.botname} 1$") == str(
            get_xmr_val(1)))
        self.assertTrue(parse_anon_tip_amount(f"anonymous tip {helper.botname} $1.0") == str(
            get_xmr_val(1)))
