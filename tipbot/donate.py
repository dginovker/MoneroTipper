import re
from decimal import Decimal

import helper
from helper import general_fund_address, format_decimal, get_signature, get_xmr_val
from logger import tipper_logger
from tipbot.backend.safewallet import SafeWallet
from tipbot.backend.transaction import generate_transaction


def parse_donate_amount(subject, sender_balance):
    """
    Parses the amount a user wishes to donate to the CSS based on their message.

    :param subject: Subject line in form "Donate xyz XMR" or "Donate xyz% of my balance"
    :param sender_balance: Their current balance, used to calculate when sending a percentage
    :return: Final amount in XMR they wish to donate
    """

    # "Donate xyz XMR"
    m = re.search('donate ([\\d\\.]+)( )?(m)?xmr', subject.lower())
    if m:
        return str(Decimal(m.group(1))/1000) if m.group(m.lastindex) == "m" else m.group(1)

    # "Donate xyz% of my balance"
    m = re.search('donate ([\\d\\.]+)% of my balance', subject.lower())
    if m:
        return str(float(m.group(1)) * float(sender_balance) / 100)

    # "Donate xyz$
    m = re.search('donate (\\$)?(?P<dollar_amt>[\\d\\.]+)(\\$)?', str(subject).lower())
    if m:
        return str(get_xmr_val(m.group("dollar_amt")))


def handle_donation(author, subject):
    """
    Allows Reddit users to donate a portion of their balance directly to the CCS
    CCS can be seen at: https://ccs.getmonero.org/

    :param author: Reddit account to withdraw from
    :param subject: Subject line of the message, telling how much to withdraw
    """

    sender_rpc_n_wallet = SafeWallet(port=helper.ports.donation_sender_port, wallet_name=author.lower())

    amount = Decimal(parse_donate_amount(subject, sender_rpc_n_wallet.wallet.balance()))

    try:
        generate_transaction(sender_wallet=sender_rpc_n_wallet.wallet, recipient_address=general_fund_address, amount=amount, split_size=1)
        helper.praw.redditor(author).message(subject="Your donation to the General Dev Fund", message=f'Thank you for donating {format_decimal(amount)} of your XMR balance to the CCS!\n\nYou will soon have your total donations broadcasted to the wiki :) {get_signature()}')
        helper.praw.redditor("OsrsNeedsF2P").message(subject=f'{author} donated {amount} to the CCS!', message="Update table here: https://old.reddit.com/r/{botname}/wiki/index#wiki_donating_to_the_ccs")
        tipper_logger.log(f'{author} donated {format_decimal(amount)} to the CCS.')
    except Exception as e:
        helper.praw.redditor(author).message(subject="Your donation to the CCS failed", message=f'Please send the following to /u/OsrsNeedsF2P:\n\n' + str(e) + get_signature())
        tipper_logger.log("Caught an error during a donation to CCS: " + str(e))

    sender_rpc_n_wallet.kill_rpc()
