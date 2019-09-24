import unittest
try:
    from unittest.mock import patch, Mock, MagicMock
except ImportError:
    from mock import patch, Mock
from main import commentRequestsTip, processMessage

class mainTestCase(unittest.TestCase):

    subject = ""
    body = ""
    author = ""
    comment = ""

    def test_comment_requests_tip(self):
        self.assertTrue(commentRequestsTip("/u/monerotipsbot 1.0 xmr monero is great"))
        self.assertFalse(commentRequestsTip(" infinity xmr"))

    def test_process_message(self):
        subject = "Withdraw .1 XMR"
        body = "44AFFq5kSiGBoZ4NMDwYtN18obc8AemS33DBLWs3H7otXft3XjrpDtQGv7SqSsaBYBb98uNbr2VBBEt7f2wfn3RVGQBEP3A"
        author = "TiedToAStar"
        comment = ""
        pass

