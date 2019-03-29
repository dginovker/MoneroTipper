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

    info_as_string = f'Public address: {info["address"]}\n\nBalance: {info["balance"]} ({info["balance_unconfirmed"]} unconfirmed){info["seed"]}'
    return info_as_string

def get_info(wallet_name, private_info=False, password="\"\""):
    """
    Gets a tuple of wallet information, based on the user's name passed in

    :param wallet_name: Name of the wallet/User who's info is being returned
    :param private_info: Boolean determining if the private mnemonic is included
    :param password: Password to open the wallet
    :return: Tuple containing the address, balance, unconfirmed balance and private seed if private_info is True
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
    Gets a tuple of wallet information, based on the wallet passed in

    :param wallet: Wallet to extract information from
    :param private_info: A boolean that determines whether or not to add the user's private info
    :return: Returns a tuple containing the user's address, balance, unconfirmed balance, and if private_info is True then their private mnemonic
    """

    return {
        "address" : str(wallet.address()),
        "balance" : format_decimal(wallet.balance(unlocked=True)),
        "balance_(unconfirmed)" : str(format_decimal(wallet.balance(unlocked=False) - wallet.balance(unlocked=True))),
        "seed" : f'\n\nPrivate mnemonic seed (DO NOT SHARE): \n\n{wallet.seed().phrase if private_info else ""}'
    }


