import unittest

import praw

import helper
import main
from tipbot import tip

try:
    from unittest.mock import patch, Mock, MagicMock
except ImportError:
    from mock import patch, Mock

class tipTestCase(unittest.TestCase):
    helper.praw = praw.Reddit("MoneroTest", user_agent='Monero non-custodial testnet tipper test suite: (by /u/OsrsNeedsF2P)')
    helper.botname = helper.praw.user.me()

    tip.handle_tip_request("MoneroTest", "/u/MoneroTest tip 0.3 XMR", None)

