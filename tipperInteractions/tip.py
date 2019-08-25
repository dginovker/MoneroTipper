from decimal import Decimal
from monero.wallet import Wallet
from monero.backends.jsonrpc import JSONRPCWallet
from wallet_rpc.rpc import RPC
from logger import tipper_logger
from helper import *
import time

from tipperInteractions.transaction import generate_transaction
from wallet_rpc.safe_wallet import safe_wallet


def get_error_response(e):
    """
    Determines the reply for an exception that occured when generating a transaction that should have been valid

    :param e: Exception to determine error for
    :return: A reply to be sent publicly to the user regarding the exception
    """
    # Default
    response = "Error: " + str(e)

    # User does not have enough inputs
    if "Method 'transfer_split' failed with RPC Error of unknown code -4" in str(e):
        response = "Sorry, you do not have enough spendable balance. Wait a bit, or see [this guide](https://www.reddit.com/r/MoneroTipsBot/wiki/index#wiki_why_is_all_my_monero_unconfirmed.3F_i_want_to_send_more_tips.21) for a solution."
    if "of unknown code -3" in str(e):
        response += "\n\n The tipbot node might be really out of sync. Checking on it soon; /u/OsrsNeedsF2P..."
    if "not enough money" in str(e) or "tx not possible" in str(e):
        response +="\n\n You do not have a high enough balance to cover the network fee. If you would like to manually withdraw the rest of your balance (<1 cent), you can try to by extracting your private key"

    return response


def tip(sender, recipient, amount, password):
    """
    Sends Monero from sender to recipient
    If the sender and the recipient are the same, it creates only 1 rpc
    Always closes RPCs, even on failure

    :param sender: name of wallet sending Monero
    :param recipient: name of wallet receiving
    :param amount: amount to send in XMR
    :return info: dictionary containing txid, a private message and a public response
    """

    if recipient == "automoderator":
        tipper_logger.log("Changing recipient to MoneroTipsBot to prevent abuse")
        recipient = "monerotipsbot"

    info = {
        "txid" : "None",
        "response" : "None",
        "message" : None
    }

    tipper_logger.log(sender + " is trying to send " + recipient + " " + amount + " XMR")

    sender = str(sender)
    recipient = str(recipient)
    sender_rpc_n_wallet = None
    recipient_rpc_n_wallet = None
    sender_port = 28088
    recipient_port = 28089

    try:
        sender_rpc_n_wallet = safe_wallet(port=sender_port, wallet_name=sender.lower(), password=password)
        if sender.lower() != recipient.lower():
            recipient_rpc_n_wallet = safe_wallet(port=recipient_port, wallet_name=recipient.lower(), password=password)
        else:
            recipient_rpc_n_wallet = sender_rpc_n_wallet
            recipient_port = sender_port
        tipper_logger.log("Wallets loaded!!")

    except Exception as e:
        sender_rpc_n_wallet.kill_rpc()
        recipient_rpc_n_wallet.kill_rpc()
        tipper_logger.log("Failed to open wallets for " + sender + " and " + recipient + ". Message: ")
        tipper_logger.log(e)
        info["response"] = "Could not open wallets properly! Perhaps my node is out of sync? (Try again shortly).\n\n^/u/OsrsNeedsF2P!!"
        info["message"] = str(e)
        return info

    tipper_logger.log("Successfully initialized wallets..")

    wallet_balance = Decimal(0) if sender_rpc_n_wallet.wallet.balance(unlocked=True) == None else sender_rpc_n_wallet.wallet.balance(unlocked=True)
    if wallet_balance + Decimal(0.00005) < Decimal(amount):
        tipper_logger.log("Can't send; " + str(wallet_balance + Decimal(0.00005)) + " is < than " + str(Decimal(amount)))
        info["response"] = "Not enough money to send! See your private message for details."
        info["message"] =  f'Not enough money to send! Need {format_decimal(Decimal(amount))}, you have {format_decimal(sender_rpc_n_wallet.wallet.balance(unlocked=True))} and {format_decimal(sender_rpc_n_wallet.wallet.balance(unlocked=False) - sender_rpc_n_wallet.wallet.balance(unlocked=True))} still incoming.'
    else:
        try:
            txs = generate_transaction(senderWallet=sender_rpc_n_wallet.wallet, recipientAddress=recipient_rpc_n_wallet.wallet.address(), amount=amount)

            info["txid"] = str(txs)
            info["response"] = "Successfully tipped /u/" + recipient + " " + amount + " XMR! [^(txid)](https://xmrchain.com/search?value=" + str(txs) + ")"
            tipper_logger.log("Successfully sent tip")
        except Exception as e:
            tipper_logger.log(e)
            info["response"] = None
            info["message"] = get_error_response(e)

    sender_rpc_n_wallet.kill_rpc()
    recipient_rpc_n_wallet.kill_rpc()

    tipper_logger.log("Tip function completed without crashing")

    return info
