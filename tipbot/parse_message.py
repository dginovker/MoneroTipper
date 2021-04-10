import re

import helper
from logger import tipper_logger
from tipbot.anon_tip import handle_anonymous_tip
from tipbot.backend.wallet_generator import generate_wallet_if_doesnt_exist
from tipbot.donate import handle_donation
from tipbot.get_info import handle_info_request
from tipbot.tip import handle_tip_request
from tipbot.withdraw import handle_withdraw_request


def comment_requests_tip(body):
    return re.search(f'(/)?u/{helper.botname.lower()} (tip )?(\\$)?([\\d\\.]+?)( )?(m)?(xmr)?(\\$)?', str(body).lower())


def subject_requests_info(subject):
    return subject.lower() in "my info"


def subject_requests_private_info(subject):
    return subject.lower() in "my private info"


def subject_requests_withdraw(subject):
    return "withdraw" in subject.lower()


def subject_requests_donate(subject):
    return "donate" in subject.lower() and "re:" not in subject.lower()


def subject_requests_anonymous_tip(subject):
    return "anonymous tip" in subject.lower() and "re:" not in subject.lower()


def process_message(author, comment, subject, body):
    """
    Handles the comment command a user tried to execute

    :param subject: Subject line of private message
    :param body: Body of private message
    :param author: Username of author
    :param comment: comment to parse for the command
    """

    tipper_logger.log(f'Received message [{subject}] from [{author}]: {body}')

    generate_wallet_if_doesnt_exist(name=author.lower(), password=helper.password)

    if comment_requests_tip(body):
        handle_tip_request(author=author, body=body, comment=comment)
        return
    if subject_requests_info(subject):
        handle_info_request(author=author, private_info=False)
        return
    if subject_requests_private_info(subject):
        handle_info_request(author=author, private_info=True)
        return
    if subject_requests_withdraw(subject):
        handle_withdraw_request(author=author, subject=subject, contents=body)
        return
    if subject_requests_donate(subject):
        handle_donation(author=author, subject=subject)
        return
    if subject_requests_anonymous_tip(subject):
        handle_anonymous_tip(author=author, subject=subject, contents=body)
        return

    helper.praw.redditor(author).message(subject="I didn't understand your command", message=f'I didn\'t understand what you meant last time you tagged me. You said: \n\n{body}\n\nIf you didn\'t mean to summon me, you\'re all good! If you\'re confused, please let my owner know by clicking Report a Bug!{helper.get_signature()}')