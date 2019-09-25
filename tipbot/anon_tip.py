import re
from _pydecimal import Decimal
from decimal import Decimal

import helper
from logger import tipper_logger
from tipbot.backend.wallet_generator import generate_wallet_if_doesnt_exist
from helper import get_xmr_val, signature
from tipbot.tip import tip


def parse_anontip_amount(subject):
    """
    :param subject: in format "Anonymous tip USER AMOUNT xmr"
    """
    m = re.search('anonymous tip [^ ]+ ([\\d\\.]+)( )?(m)?xmr', subject.lower())
    if m:
        return str(Decimal(m.group(1))/1000) if m.group(m.lastindex) == 'm' else m.group(1)

    m = re.search('anonymous tip [^ ]+ (\\$)?(?P<dollar_amt>[\\d\\.]+)(\\$)?', str(subject).lower())
    if m:
        return str(get_xmr_val(m.group("dollar_amt")))


def parse_anontip_recipient(subject):
    """
    :param subject: in format "Anonymous tip USER AMOUNT xmr"
    """
    m = re.search('anonymous tip (.+) .+ (m)?xmr', subject.lower())
    if m:
        generate_wallet_if_doesnt_exist(m.group(1).lower(), helper.bot_handler.password)
        if m.group(1) == "automoderator":
            return "monerotipsbot"
        return m.group(1)


def handle_anonymous_tip(bot_handler, author, subject, contents):
    """
    Allows people to send anonymous tips

    :param author: Reddit account to withdraw from
    :param subject: Subject line of the message, telling who to tip and how much
    :param contents: Message body (ignored)
    """

    recipient = parse_anontip_recipient(subject)
    amount = parse_anontip_amount(subject)

    if recipient is None or amount is None:
        helper.bot_handler.reddit.redditor(author.name).message(subject="Your anonymous tip", message="Nothing interesting happens.\n\n*Your recipient or amount wasn't clear to me*" + signature)
        return
    if Decimal(amount) < 0.001: #  Less than amount displayed in balance page
        helper.bot_handler.reddit.redditor(author.name).message(subject="Your anonymous tip", message=helper.bot_handler.below_threshold_message + signature)
        return

    tipper_logger.log(author.name + " is trying to send " + parse_anontip_amount(subject) + " XMR to " + parse_anontip_recipient(subject))
    res = tip(sender=author.name, recipient=recipient, amount=amount, password=helper.bot_handler.password)
    if res["message"] is not None:
        helper.bot_handler.reddit.redditor(author.name).message(subject="Your anonymous tip", message=res["message"] + signature)
    else:
        helper.bot_handler.reddit.redditor(author.name).message(subject="Anonymous tip successful",  message=res["response"] + signature)
        recipient_message = signature if contents == "Edit this line to send a message, or leave it exactly the same to attach no message at all!" else "The tipper attached the following message:\n\n" + contents + signature
        helper.bot_handler.reddit.redditor(recipient).message("You have recieved an anonymous tip of " + amount + " XMR!", message=recipient_message)