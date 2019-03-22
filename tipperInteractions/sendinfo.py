from monero.wallet import Wallet
from monero.backends.jsonrpc import JSONRPCWallet
from monero.seed import Seed
from moneroRPC.rpc import RPC
import time

def sendinfo(walletName):
    """
    Displays the wallet addresses and contents to the user

    :param wallet Reddit username to gather information about
    :return formatted string of content
    """

    rpcP = RPC(port=28088, walletfile=walletName)

    time.sleep(10)

    wallet = Wallet(JSONRPCWallet(port=28088))


    info = "Public address: " + str(wallet.address()) + "\nBalance: " + str(wallet.balance(True)) + " (+ " + str(wallet.balance(False) - wallet.balance(True)) + " unconfirmed)\nPrivate mnemonic (DO NOT SHARE): " + wallet.seed().phrase

    rpcP.kill()
    return info