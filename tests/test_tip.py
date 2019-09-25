import unittest
from decimal import Decimal
import decimal

try:
    from unittest.mock import patch, Mock, MagicMock
except ImportError:
    from mock import patch, Mock
from tipbot.tip import tip

class tipTestCase(unittest.TestCase):
    accounts_result = {'id': 0,
                       'jsonrpc': '2.0',
                       'result': {'subaddress_accounts': [{'account_index': 0,
                                                           'balance': 224916129245183,
                                                           'base_address': '9vgV48wWAPTWik5QSUSoGYicdvvsbSNHrT9Arsx1XBTz6VrWPSgfmnUKSPZDMyX4Ms8R9TkhB4uFqK9s5LUBbV6YQN2Q9ag',
                                                           'label': 'Primary account',
                                                           'unlocked_balance': 224916129245183},
                                                          {'account_index': 1,
                                                           'balance': 3981420960933,
                                                           'base_address': 'BaCBwYSK9BGSuKxb2msXEj4mmpvZYJexYHfqx7kNPDrXDePVXSfoofxGquhXxpA4uxawcnVnouusMDgP74CACa7e9siimpj',
                                                           'label': 'Untitled account',
                                                           'unlocked_balance': 3981420960933},
                                                          {'account_index': 2,
                                                           'balance': 7256159239955,
                                                           'base_address': 'BgCseuY3jFJAZS7kt9mrNg7fEG3bo5BV91CTyKbYu9GFiU6hUZhvdNWCTUdQNPNcA4PyFApsFr3EsQDEDfT3tQSY1mVZeP2',
                                                           'label': 'Untitled account',
                                                           'unlocked_balance': 7256159239955}],
                                  'total_balance': 236153709446071,
                                  'total_unlocked_balance': 236153709446071}}

    @patch('logger.tipper_logger.log')
    @patch('monero.backends.jsonrpc.requests.post')
    @patch('tipbot.tip.RPC')
    def test_tip(self, mock_logger, mock_post, mock_rpc):
        mock_rpc.return_value = MagicMock()
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = self.accounts_result
        # this is an example of a currently unhandled exception
        # if you have: "/u/monerotipsbot . xmr I hate this monero community member" in the body, regex parses the amount as a string "."
        #self.assertRaises(decimal.InvalidOperation, tip, "sender", "recipient", ".", "password")
        pass