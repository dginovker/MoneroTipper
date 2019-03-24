from monero.wallet import Wallet
from monero.backends.jsonrpc import JSONRPCWallet
from moneroRPC.rpc import RPC
from decimal import Decimal
from helper import *
import time


def tip(sender, recipient, amount):
    """
    Sends Monero from sender to recipient

    :param sender: wallet sending Monero
    :param recipient: wallet receiving
    :param amount: amount to send in XMR
    :return info: dictionary of the txid and message
    """

    recipient = str(recipient)
    sender = str(sender)

    rpcPsender = RPC(port=28088, wallet_file=sender)
    rpcPrecipient = RPC(port=28089, wallet_file=recipient)

    time.sleep(10)

    senderWallet = Wallet(JSONRPCWallet(port=28088))
    recipientWallet = Wallet(JSONRPCWallet(port=28089))


    info = {
        "txid" : "None",
        "message" : "None",
    }

    #print("Recipient address: ", recipientWallet.address(), "\nSender balance: ", senderWallet.balance())

    if senderWallet.balance(unlocked=True) >= Decimal(amount):
        print(sender + " is trying to send " + recipient + " " + amount + " XMR")
        try:
            txs = senderWallet.transfer(recipientWallet.address(), Decimal(amount))
            info["txid"] = str(txs)
            info["message"] = "Successfully tipped /u/" + sender + " " + amount + " XMR!"
        except Exception as e:
            print(e)
            info["message"] = "Error: " + str(e)
    else:
        info["message"] = "Not enough money to send! Need " + format_decimal(Decimal(amount)) + ", has " + format_decimal(senderWallet.balance(unlocked=True)) + " and " + format_decimal(senderWallet.balance(unlocked=False)) + " still incoming"

    rpcPsender.kill()
    rpcPrecipient.kill()


    return info