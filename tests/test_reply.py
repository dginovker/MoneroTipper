import unittest
import helper
from decimal import Decimal
import decimal

from tipbot.tip import parse_tip_amount

try:
    from unittest.mock import patch, Mock, MagicMock
except ImportError:
    from mock import patch, Mock

class replyTestCase(unittest.TestCase):
    author = ""
    body = ""
    comment = ""
    subject = ""

    def test_parse_tip_amount(self):
        body = f"/u/{helper.botname.lower()} 1.0 xmr I love this monero community member"
        self.assertEqual(parse_tip_amount(body, self.replier.botname), "1.0")

    @patch('logger.tipper_logger.log')
    @patch('tipbot.wallet_generator.generate_wallet_if_doesnt_exist')
    def test_handle_tip_request(self, mock_logger, mock_generate_wallet_if_doesnt_exist):
        pass
        #author = MagicMock()
        #author.return_value="/u/tiedtoastar"
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