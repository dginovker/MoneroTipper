from monero.wallet import Wallet
from monero.backends.jsonrpc import JSONRPCWallet
from moneroRPC.rpc import RPC
from decimal import Decimal
import time, json
import pprint


def tip(sender, recipient, amount):
    """
    Sends Monero from sender to recipient

    :param sender: wallet sending Monero
    :param recipient: wallet receiving
    :param amount: amount to send in XMR
    :return info: dictionary of the txid and message
    """

    rpcPsender = RPC(port=28088, walletfile=sender)
    rpcPrecipient = RPC(port=28089, walletfile=recipient)

    time.sleep(10)

    senderWallet = Wallet(JSONRPCWallet(port=28088))
    recipientWallet = Wallet(JSONRPCWallet(port=28089))


    info = {
        "txid" : "None",
        "message" : "None",
    }

    #print("Recipient address: ", recipientWallet.address(), "\nSender balance: ", senderWallet.balance())

    if senderWallet.balance(unlocked=True) >= Decimal(amount):
        txs = senderWallet.transfer(recipientWallet.address(), Decimal(amount))
        info["txid"] = txs
        info["message"] = "Success"
    else:
        info["message"] = "Not enough money to send! Need " + amount + ", has " + str(senderWallet.balance(unlocked=True)) + " and " + str(senderWallet.balance(unlocked=False)) + " still incoming"

    rpcPsender.kill()
    rpcPrecipient.kill()


    return info