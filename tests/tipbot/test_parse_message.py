import unittest

import helper
from tipbot.parse_message import comment_requests_tip

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

    def test_comment_requests_tip(self):
        self.assertTrue(comment_requests_tip(f"/u/{helper.botname} 1 XMR"))
        self.assertTrue(comment_requests_tip(f"/u/{helper.botname} 1xmr"))
        self.assertTrue(comment_requests_tip(f"/u/{helper.botname} 1mXMR"))
        self.assertTrue(comment_requests_tip(f"/u/{helper.botname} 1$"))
        self.assertTrue(comment_requests_tip(f"/u/{helper.botname} $1"))
        self.assertTrue(comment_requests_tip(f"thx for the guide /u/{helper.botname} tip 1mxmr enjoy :)"))
