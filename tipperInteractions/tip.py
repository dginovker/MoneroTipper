from monero.wallet import Wallet
from monero.backends.jsonrpc import JSONRPCWallet
from moneroRPC.rpc import RPC
from decimal import Decimal
import time


def tip(sender, recipient, amount):
    """
    Sends Monero from sender to recipient

    :param sender: wallet sending Monero
    :param recipient: wallet receiving
    :param amount: amount to send in XMR
    """
    start = time.time()

    rpcPsender = RPC(port=28088, walletfile=sender)
    rpcPrecipient = RPC(port=28089, walletfile=recipient)

    time.sleep(10)

    senderWallet = Wallet(JSONRPCWallet(port=28088))
    recipientWallet = Wallet(JSONRPCWallet(port=28089))

    print("It took", time.time() - start, "to get both wallets.")

    start = time.time()

    print("Recipient address: ", recipientWallet.address(), "\nSender balance: ", senderWallet.balance())

    if (senderWallet.balance(unlocked=True) >= amount):
        txs = senderWallet.transfer(recipientWallet.address(), Decimal(amount))
    else:
        print("Not enough money to send! Need ", amount, ", has ", senderWallet.balance(unlocked=True), "and", senderWallet.balance(unlocked=False), " still incoming")

    rpcPsender.kill()
    rpcPrecipient.kill()

    end = time.time()

    print("It has since taken", end - start, " to do all my things")
