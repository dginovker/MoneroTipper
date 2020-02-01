import unittest

import helper

try:
    from unittest.mock import patch, Mock, MagicMock
except ImportError:
    from mock import patch, Mock

class mainTestCase(unittest.TestCase):

    helper.botname = "MoneroTip"
