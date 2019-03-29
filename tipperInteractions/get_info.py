from monero.wallet import Wallet
from monero.backends.jsonrpc import JSONRPCWallet
from moneroRPC.rpc import RPC
from helper import *
import time

from tipperInteractions.wallet_generator import generate_wallet_if_doesnt_exist


def get_info_as_string(wallet_name, private_info=False, password="\"\""):
    """
    Displays the wallet addresses and contents to the user

    :param wallet Reddit username to gather information about
    :return formatted string of content
    """

    info = get_info(wallet_name, private_info, password)

    info_as_string = "Public address: " + info["address"] + "\n\nBalance: " + info["balance"] + " (+ " + info["balance"] + " unconfirmed)" + info["seed"]
    return info_as_string

def get_info(wallet_name, private_info=False, password="\"\""):
    """

    :param wallet_name:
    :param private_info:
    :param password:
    :return:
    """

    generate_wallet_if_doesnt_exist(wallet_name, password)

    rpcP = RPC(port=28088, wallet_file=wallet_name, password=password)

    time.sleep(10)
    wallet = Wallet(JSONRPCWallet(port=28088, password=password))

    info = get_info_from_wallet(wallet, private_info)

    rpcP.kill()
    return info


def get_info_from_wallet(wallet, private_info=False):
    """

    :param wallet:
    :param private_info:
    :return:
    """

    return {
        "address" : str(wallet.address()),
        "balance" : format_decimal(wallet.balance(True)),
        "balance_(unconfirmed)" : str(format_decimal(wallet.balance(False) - wallet.balance(True))),
        "seed" : ("\n\nPrivate mnemonic seed (DO NOT SHARE): \n\n" + str(wallet.seed().phrase) if private_info else "")
    }


