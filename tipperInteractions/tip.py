from monero.wallet import Wallet
from monero.backends.jsonrpc import JSONRPCWallet
from moneroRPC.rpc import RPC
from helper import *
import time


def tip(sender, recipient, amount, password):
    """
    Sends Monero from sender to recipient

    :param sender: wallet sending Monero
    :param recipient: wallet receiving
    :param amount: amount to send in XMR
    :return info: dictionary of the txid and message
    """

    recipient = str(recipient)
    sender = str(sender)

    rpcPsender = RPC(port=28088, wallet_file=sender, password=password)
    rpcPrecipient = RPC(port=28089, wallet_file=recipient, password=password)

    time.sleep(10)

    senderWallet = Wallet(JSONRPCWallet(port=28088, password=password))
    recipientWallet = Wallet(JSONRPCWallet(port=28089, password=password))


    info = {
        "txid" : "None",
        "message" : "None",
    }

    #print("Recipient address: ", recipientWallet.address(), "\nSender balance: ", senderWallet.balance())

    if senderWallet.balance(unlocked=True) >= Decimal(amount):
        print(sender + " is trying to send " + recipient + " " + amount + " XMR")
        try:
            txs = senderWallet.transfer(recipientWallet.address(), Decimal(amount))
            info["txid"] = "https://testnet.xmrchain.com/search?value=" + str(txs)
            info["message"] = "Successfully tipped /u/" + recipient + " " + amount + " XMR!"
        except Exception as e:
            print(e)
            info["message"] = "Error: " + str(e)
            if "Method 'transfer_split' failed with RPC Error of unknown code -4" in str(e):
                info["message"] = "Error: You do not have enough spendable balance. Either wait a bit, or see [this link](https://www.reddit.com/r/MoneroTipsBot/wiki/index#wiki_why_is_all_my_monero_unconfirmed.3F_i_want_to_send_more_tips.21) on how to avoid this in the future."
    else:
        info["message"] = "Not enough money to send! Need " + format_decimal(Decimal(amount)) + ", has " + format_decimal(senderWallet.balance(unlocked=True)) + " and " + format_decimal(senderWallet.balance(unlocked=False)) + " still incoming"

    rpcPsender.kill()
    rpcPrecipient.kill()


    return info