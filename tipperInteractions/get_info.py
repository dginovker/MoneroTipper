from monero.wallet import Wallet
from monero.backends.jsonrpc import JSONRPCWallet
from moneroRPC.rpc import RPC
from helper import *
import time

from tipperInteractions.wallet_generator import generate_wallet_if_doesnt_exist


def get_info(wallet_name, private_info=False):
    """
    Displays the wallet addresses and contents to the user

    :param wallet Reddit username to gather information about
    :return formatted string of content
    """

    generate_wallet_if_doesnt_exist(wallet_name)

    rpcP = RPC(port=28088, wallet_file=wallet_name)

    time.sleep(10)

    wallet = Wallet(JSONRPCWallet(port=28088))


    info = "Public address: " + str(wallet.address()) + "\n\nBalance: " + format_decimal(wallet.balance(True)) + " (+ " + format_decimal(wallet.balance(False) - wallet.balance(True)) + " unconfirmed)" + ("\n\nPrivate mnemonic seed (DO NOT SHARE): \n\n" + str(wallet.seed().phrase) if private_info else "") + signature

    rpcP.kill()
    return info