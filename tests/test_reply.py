import unittest
from decimal import Decimal
import decimal
try:
    from unittest.mock import patch, Mock, MagicMock
except ImportError:
    from mock import patch, Mock
from tipperInteractions.reply import ReplyHandler

class replyTestCase(unittest.TestCase):
    author = ""
    body = ""
    comment = ""
    subject = ""

    def setUp(self):
        self.replier = ReplyHandler(reddit=MagicMock(), password="password")
        pass

    def test_parse_tip_amount(self):
        body = "/u/monerotipsbot 1.0 xmr I love this monero community member"
        self.assertEqual(self.replier.parse_tip_amount(body), "1.0")

    @patch('logger.tipper_logger.log')
    @patch('tipperInteractions.wallet_generator.generate_wallet_if_doesnt_exist')
    def test_handle_tip_request(self, mock_logger, mock_generate_wallet_if_doesnt_exist):
        pass
        #author = MagicMock()
        #author.name.return_value="/u/tiedtoastar"
        #body = "/u/monerotipsbot 1.0 xmr monero is great"
        #comment = MagicMock()
        #comment.parent.author.return_value="/u/OsrsNeedsF2P"
        #self.replier.handle_tip_request(author, body, comment)

    def test_handle_info_request(self):
        author = ""
        #self.replier.handle_info_request(author=author, private_info=False)
        pass

    def test_handle_info_request_private(self):
        author = ""
        #self.replier.handle_info_request(author=author, private_info=True)
        pass

    def test_handle_withdraw_request(self):
        author = ""
        body = ""
        subject = ""
        #self.replier.handle_withdraw_request(author=author, subject=subject, contents=body)
        pass

    def test_handle_donation(self):
        author = ""
        body = ""
        subject = ""
        #self.replier.handle_donation(author=author, subject=subject, contents=body)
        pass

    def test_handle_private_tip(self):
        author = ""
        body = ""
        subject = ""
        #self.replier.handle_private_tip(author=author, subject=subject, contents=body)
        pass