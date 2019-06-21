from decimal import Decimal

from logger import tipper_logger
from tipperInteractions.get_info import get_info_from_wallet
from tipperInteractions.transaction import generate_transaction
from tipperInteractions.tip import get_error_response

from helper import *


def handle_withdraw(sender_wallet, sender_name, recipient_address, amount):
    """
    Withdraws Monero from sender_name's wallet

    :param sender_wallet: sender_name's wallet
    :param sender_name: User who wishes to withdraw
    :param recipient_address: Address to send funds to
    :param amount: Amount to send in XMR
    :return: Response message regarding status of send
    """

    res = ""

    if sender_wallet.balance(unlocked=True) >= Decimal(amount):
        tipper_logger.log(f'{sender_name} is trying to send {recipient_address} {amount} XMR')
        try:
            res = "Withdrawl success! [Txid](https://xmrchain.net/search?value="
            res += generate_transaction(senderWallet=sender_wallet, recipientAddress=recipient_address,
                                        amount=Decimal(amount))
            res += ")"
        except Exception as e:
            tipper_logger.log(e)
            res = get_error_response(e)
    else:
        walletInfo = get_info_from_wallet(sender_wallet)
        res = f'Not enough money to send! Need {format_decimal(Decimal(amount))}, has {walletInfo["balance"]} and {walletInfo["balance_(unconfirmed)"]} still incoming.'

    return res
