import unittest

import praw

import helper
from tipbot import tip

from unittest.mock import patch, Mock, MagicMock

class tipTestCase(unittest.TestCase):
    helper.praw = praw.Reddit("MoneroTest", user_agent='Monero non-custodial testnet tipper test suite: (by /u/OsrsNeedsF2P)')
    helper.botname = helper.praw.user.me()

    tip.handle_tip_request("MoneroTest", "/u/MoneroTest tip 0.3 XMR", None)

