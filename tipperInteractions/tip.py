from decimal import Decimal
from monero.wallet import Wallet
from monero.backends.jsonrpc import JSONRPCWallet
from moneroRPC.rpc import RPC
from logger import tipper_logger
from helper import *
import time

from tipperInteractions.transaction import generate_transaction


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
        response = "Congradulations, I tried to fix this. Pinging me: /u/OsrsNeedsF2P\n\nCould you please tell how much did you thought you had available to tip, and how many tips you've issued in the past 20 minutes? Thanks\n\nError: You do not have enough spendable balance. Either wait a bit, or see [this link](https://www.reddit.com/r/MoneroTipsBot/wiki/index#wiki_why_is_all_my_monero_unconfirmed.3F_i_want_to_send_more_tips.21) on how to avoid this in the future."
    if "of unknown code -3" in str(e):
        response += "\n\n The tipbot node might be really out of sync. Checking on it soon"

    return response + "\n\n /u/OsrsNeedsF2P..."


def get_balance_too_low_message(senderWallet, amount):
    """
    Determines the private message to send to a user who tried to tip more than their balance

    :param senderWallet:
    :param amount:
    :return:
    """

    message = f'Not enough money to send! Need {format_decimal(Decimal(amount))}, you have {format_decimal(senderWallet.balance(unlocked=True))} and {format_decimal(senderWallet.balance(unlocked=False))} still incoming.'
    if senderWallet.balance(unlocked=True) == 0 and senderWallet.balance(unlocked=False) > 0:
        message += "\n\n[(Why is all my balance still incoming?)](https://www.reddit.com/r/MoneroTipsBot/wiki/index#wiki_why_is_all_my_monero_unconfirmed.3F_i_want_to_send_more_tips.21)"

    return message


def tip(sender, recipient, amount, password):
    """
    Sends Monero from sender to recipient
    If the sender and the recipient are the same, it creates only 1 rpc
    Always closes RPCs, even on failure

    :param sender: wallet sending Monero
    :param recipient: wallet receiving
    :param amount: amount to send in XMR
    :return info: dictionary containing txid, a private message and a public response
    """

    info = {
        "txid" : "None",
        "response" : "None",
        "message" : None
    }

    tipper_logger.log(sender + " is trying to send " + recipient + " " + amount + " XMR")

    recipient = str(recipient)
    sender = str(sender)
    rpcPrecipient = None
    rpcPsender = None
    sender_port = 28088
    recipient_port = 28089

    try:
        rpcPsender = RPC(port=sender_port, wallet_file=sender, password=password)
        if sender != recipient:
            rpcPrecipient = RPC(port=recipient_port, wallet_file=recipient, password=password)
        else:
            rpcPrecipient = rpcPsender
            recipient_port = sender_port

        print("We're loaded!!")

        senderWallet = Wallet(JSONRPCWallet(port=sender_port, password=password))
        recipientWallet = Wallet(JSONRPCWallet(port=recipient_port, password=password))
    except Exception as e:
        tipper_logger.log(e)
        tipper_logger.log("Failed to open wallets for " + sender + " and " + recipient)
        info["response"] = "Could not open wallets properly! Perhaps my node is out of sync? (Try again shortly).\n\n^/u/OsrsNeedsF2P!!"
        info["message"] = str(e)
        rpcPsender.kill()
        rpcPrecipient.kill()
        return info

    tipper_logger.log("Successfully initialized wallets..")

    wallet_balance = Decimal(0) if senderWallet.balance(unlocked=True) == None else senderWallet.balance(unlocked=True)
    if wallet_balance < Decimal(amount):
        tipper_logger.log("Can't send; " + str(wallet_balance) + " is < than " + str(amount))
        info["response"] = "Not enough money to send! See your private message for details."
        info["message"] = get_balance_too_low_message(senderWallet, amount)
    else:
        try:
            txs = generate_transaction(senderWallet=senderWallet, recipientAddress=recipientWallet.address(), amount=amount)

            info["txid"] = "https://testnet.xmrchain.com/search?value=" + str(txs)
            info["response"] = "Successfully tipped /u/" + recipient + " " + amount + " tXMR!"
            tipper_logger.log("Successfully sent tip")
        except Exception as e:
            tipper_logger.log(e)
            info["response"] = get_error_response(e)
            info["message"] = None

    rpcPsender.kill()
    rpcPrecipient.kill()

    tipper_logger.log("Tip function completed without crashing")

    return info