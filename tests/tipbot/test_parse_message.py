import unittest

import helper
from tipbot.parse_message import comment_requests_tip, subject_requests_anonymous_tip, subject_requests_info, \
    subject_requests_private_info, subject_requests_donate, subject_requests_withdraw


def only(pass_function, message):
    fail_functions = [subject_requests_info, subject_requests_private_info, subject_requests_withdraw, subject_requests_donate, subject_requests_anonymous_tip]
    fail_functions.remove(pass_function)

    for fail_function in fail_functions:
        if (fail_function(message)):
            return False

    return pass_function(message)

class mainTestCase(unittest.TestCase):

    helper.botname = "MoneroTip"

    def test_comment_requests_tip(self):
        self.assertTrue(comment_requests_tip(f"/u/{helper.botname} 1 XMR"))
        self.assertTrue(comment_requests_tip(f"/u/{helper.botname} 1xmr"))
        self.assertTrue(comment_requests_tip(f"/u/{helper.botname} 1 mXMR"))
        self.assertTrue(comment_requests_tip(f"/u/{helper.botname} 1$"))
        self.assertTrue(comment_requests_tip(f"/u/{helper.botname} $1"))
        self.assertTrue(comment_requests_tip(f"thx for the guide /u/{helper.botname} tip 1mxmr enjoy :)"))

        self.assertTrue(comment_requests_tip(f"/u/{helper.botname} $0.03"))

        self.assertFalse(comment_requests_tip(f"/u/{helper.botname}'s broken"))

    def test_subject_requests_info(self):
        self.assertTrue(only(subject_requests_info, "my info"))

    def test_subject_requests_private_info(self):
        self.assertTrue(only(subject_requests_private_info, "my private info"))

    def test_subject_requests_withdraw(self):
        self.assertTrue(only(subject_requests_withdraw, "withdraw 5 xmr"))
        self.assertTrue(only(subject_requests_withdraw, "withdraw $5"))
        self.assertTrue(only(subject_requests_withdraw, "withdraw 5.00$"))

    def test_subject_requests_donate(self):
        self.assertTrue(only(subject_requests_donate, "donate 5 xmr"))
        self.assertTrue(only(subject_requests_donate, "donate 5 xmr"))

        self.assertFalse(subject_requests_donate("re: donate 5 xmr"))

    def test_comment_requests_anon_tip(self):
        self.assertTrue(only(subject_requests_anonymous_tip, f"anonymous tip /u/{helper.botname} $5.00"))
        self.assertTrue(only(subject_requests_anonymous_tip, f"anonymous tip /u/{helper.botname} 5.00 xmr"))

        self.assertFalse(subject_requests_anonymous_tip(f"re: You have received an anonymous tip of 0.01 XMR!"))
        self.assertFalse(subject_requests_anonymous_tip(f"re: anonymous tip /u/{helper.botname} 5.00$"))
