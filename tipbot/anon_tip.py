import re
from decimal import Decimal

import helper
from helper import get_signature
from logger import tipper_logger
from tipbot.backend.wallet_generator import generate_wallet_if_doesnt_exist
from helper import get_xmr_val
from tipbot.tip import tip, fix_automoderator_recipient


def parse_anon_tip_amount(subject):
    """
    Returns amount of XMR to tip

    :param subject: in format "Anonymous tip USER AMOUNT xmr"
    """
    m = re.search('anonymous tip [^ ]+ ([\\d\\.]+)( )?(m)?xmr', subject.lower())
    if m:
        return str(Decimal(m.group(1)) / 1000) if m.group(m.lastindex) == 'm' else m.group(1)

    m = re.search('anonymous tip [^ ]+ (\\$)?(?P<dollar_amt>[\\d\\.]+)(\\$)?', str(subject).lower())
    if m:
        return str(get_xmr_val(m.group("dollar_amt")))


def parse_anon_tip_recipient(subject):
    """
    Returns username as String to send XMR to

    :param subject: in format "Anonymous tip USER AMOUNT xmr"
    """
    m = re.search('anonymous tip ([^\s]+) .+ (m)?xmr', subject.lower())
    if m:
        return fix_automoderator_recipient(m.group(1))


def handle_anonymous_tip(author, subject, contents):
    """
    Allows people to send anonymous tips

    :param author: Reddit account to withdraw from
    :param subject: Subject line of the message, telling who to tip and how much
    :param contents: Message body (ignored)
    """

    recipient = parse_anon_tip_recipient(subject)
    amount = parse_anon_tip_amount(subject)

    if recipient is None or amount is None:
        helper.praw.redditor(author).message(subject="Your anonymous tip", message="Nothing interesting happens.\n\n*Your recipient or amount wasn't clear to me*" + get_signature())
        return
    if Decimal(amount) < (0.0001):  # Less than amount displayed in balance page
        helper.praw.redditor(author).message(subject="Your anonymous tip", message=helper.get_below_threshold_message() + get_signature())
        return

    generate_wallet_if_doesnt_exist(recipient)

    tipper_logger.log(author + " is trying to send " + parse_anon_tip_amount(subject) + " XMR to " + parse_anon_tip_recipient(subject))

    res = tip(sender=author, recipient=recipient, amount=amount)

    if res["message"] is not None:
        helper.praw.redditor(author).message(subject="Your anonymous tip", message=res["message"] + get_signature())
    else:
        helper.praw.redditor(author).message(subject="Anonymous tip successful", message=res["response"] + get_signature())
        helper.praw.redditor(recipient).message("You have received an anonymous tip of " + amount + " XMR!",
                                                message=(get_signature() if contents == helper.no_message_anon_tip_string else "The tipper attached the following message:\n\n" + contents + get_signature()))
