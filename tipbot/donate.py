from decimal import Decimal

import helper
from helper import format_decimal, get_signature
from logger import tipper_logger
from tipbot.backend.safewallet import SafeWallet
from tipbot.backend.transaction import generate_transaction


def handle_donation(author, subject):
    """
    Allows Reddit users to donate a portion of their balance directly to the CCS
    CCS can be seen at: https://ccs.getmonero.org/

    :param author: Reddit account to withdraw from
    :param subject: Subject line of the message, telling how much to withdraw
    """

    sender_rpc_n_wallet = SafeWallet(port=helper.ports.donation_sender_port, wallet_name=author.lower(), wallet_password=helper.password)

    amount = Decimal(helper.parse_amount('donate ', subject, balance=sender_rpc_n_wallet.wallet.balance()))

    try:
        generate_transaction(sender_wallet=sender_rpc_n_wallet.wallet, recipient_address=helper.get_general_fund_address(), amount=amount, split_size=1)
        helper.praw.redditor(author).message(subject="Your donation to the General Dev Fund", message=f'Thank you for donating {format_decimal(amount)} of your XMR balance to the CCS!\n\nYou will soon have your total donations broadcasted to the wiki :) {get_signature()}')
        helper.praw.redditor("OsrsNeedsF2P").message(subject=f'{author} donated {amount} to the CCS!', message=f"Update table here: https://old.reddit.com/r/{helper.botname}/wiki/index#wiki_donating_to_the_ccs")
        tipper_logger.log(f'{author} donated {format_decimal(amount)} to the CCS.')
    except Exception as e:
        helper.praw.redditor(author).message(subject="Your donation to the CCS failed", message=f'Please send the following to /u/OsrsNeedsF2P:\n\n' + str(e) + get_signature())
        tipper_logger.log("Caught an error during a donation to CCS: " + str(e))

    sender_rpc_n_wallet.kill_rpc()
