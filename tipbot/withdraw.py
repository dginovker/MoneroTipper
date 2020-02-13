import re
from decimal import Decimal

import helper
from logger import tipper_logger
from tipbot.backend.safewallet import SafeWallet
from tipbot.backend.transaction import generate_transaction
from helper import get_xmr_val, get_signature
from tipbot.tip import get_error_response


def handle_withdraw(sender_wallet, sender_name, recipient_address, amount):
    """
    Withdraws Monero from sender_name's wallet

    :param sender_wallet: sender_name's wallet
    :param sender_name: User who wishes to withdraw
    :param recipient_address: Address to send funds to
    :param amount: Amount to send in XMR
    :return: Response message regarding status of send
    """

    tipper_logger.log(f'{sender_name} is trying to send {recipient_address} {amount} XMR')
    try:
        res = "Withdrawal success! [Txid](" \
              f"{helper.get_xmrchain(generate_transaction(sender_wallet=sender_wallet, recipient_address=recipient_address, amount=Decimal(amount)))})"
    except Exception as e:
        tipper_logger.log(e)
        res = get_error_response(e)

    return res


def handle_withdraw_request(author, subject, contents):
    """
    Handles the withdrawal request, setting up RPC and calling the withdraw function

    :param author: Wallet to withdraw from
    :param subject: The withdrawl request string
    :param contents: The address to withdraw to
    :return: Response message about withdrawl request
    """

    amount = helper.parse_amount("withdraw ", subject)
    if amount is None:
        helper.praw.redditor(author).message(subject="I didn't understand your withdrawal!", message=f'You sent: "{subject}", but I couldn\'t figure out how much you wanted to send. See [this](https://www.reddit.com/r/{helper.botname}/wiki/index#wiki_withdrawing) guide if you need help, or click "Report a Bug" under "Get Started"  if you think there\'s a bug!' + get_signature())
        return None

    sender_rpc_n_wallet = SafeWallet(port=helper.ports.withdraw_sender_port, wallet_name=author.lower(), wallet_password=helper.password)

    res = str(handle_withdraw(sender_rpc_n_wallet.wallet, author, contents, amount))

    sender_rpc_n_wallet.kill_rpc()

    helper.praw.redditor(author).message(subject="Your withdrawl", message=res + get_signature())
    tipper_logger.log("Told " + author + " their withdrawl status (" + res + ")")
