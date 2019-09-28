from decimal import Decimal

import helper
from helper import get_signature
from logger import tipper_logger

from tipbot.backend.wallet_generator import generate_wallet_if_doesnt_exist
from tipbot.backend.safewallet import SafeWallet


def get_info_as_string(wallet_name, private_info=False):
    """
    Displays the wallet addresses and contents to the user

    :param wallet_name: Name of wallet to open
    :param private_info: Whether to return wallet's seed
    :return formatted string of content
    """

    info = get_info(wallet_name=wallet_name, private_info=private_info, password=helper.password)

    info_as_string = f'Public address: {info["address"]} [(QR code)](https://api.qrserver.com/v1/create-qr-code/?data={info["address"]}&size=220x220&margin=4)\n\nBalance: {info["balance"]} ({info["balance_(unconfirmed)"]} unconfirmed)\n\n{info["seed"]}'
    return info_as_string


def get_info(wallet_name, private_info=False, port=helper.ports.get_info_port, password=helper.password, timeout=300):
    """
    Gets a tuple of wallet information, based on the user's name passed in

    :param wallet_name: Name of the wallet/User who's info is being returned
    :param private_info: Boolean determining if the private mnemonic is included
    :param port: Port to tell safe_wallet to open on
    :param password: Password to open the wallet
    :param timeout: Time until RPC is aborted
    :return: Tuple containing the address, balance, unconfirmed balance and private seed if private_info is True
    """

    generate_wallet_if_doesnt_exist(wallet_name)

    rpc_n_wallet = SafeWallet(port=port, wallet_name=wallet_name, password=password, timeout=timeout)

    info = get_info_from_wallet(rpc_n_wallet.wallet, wallet_name, private_info)

    rpc_n_wallet.kill_rpc()
    return info


def get_balance(wallet, confirmed):
    """
    Gets sentence describing wallet balance

    :param wallet: Wallet to check balance
    :param confirmed: Getting confirmed balance or not
    :return: Returns either confirmed or unconfirmed balance, with additional note if balance is too low to present but exists
    """
    conf_balance = wallet.balance(unlocked=True)
    unconf_balance = wallet.balance(unlocked=False) - wallet.balance(unlocked=True)
    dust_message = ""

    if Decimal(0) < conf_balance < 0.0001:
        dust_message += " (Miniscule balance exists, export private key to view it)"
    if Decimal(0) < unconf_balance < 0.0001:
        dust_message += " (Miniscule unconf balance exists, export private key to view it)"

    return helper.format_decimal(conf_balance) + dust_message if confirmed \
        else helper.format_decimal(unconf_balance) + dust_message


def get_info_from_wallet(wallet, wallet_name, private_info=False):
    """
    Gets a tuple of wallet information, based on the wallet passed in

    :param wallet_name: Username/wallet name
    :param wallet: Wallet object to extract information from
    :param private_info: A boolean that determines whether or not to add the user's private info
    :return: Returns a tuple containing the user's address, balance, unconfirmed balance, and if private_info is True then their private mnemonic
    """
    return {
        "address": str(wallet.address()),
        "balance": get_balance(wallet, True),  # format_decimal(wallet.balance(unlocked=True)),
        "balance_(unconfirmed)": str(helper.format_decimal(wallet.balance(unlocked=False) - wallet.balance(unlocked=True))),
        "seed": "Private mnemonic seed: " + wallet.seed().phrase + "\n\nRestore height (optional): " + open(
            "wallets/" + wallet_name + ".height", "r").read() if private_info
        else "If you would like your **private** info, click [here](https://www.reddit.com/r/{botname}/wiki/index#wiki_extracting_your_private_key)"
    }


def handle_info_request(author, private_info=False):
    """
    Allows Reddit users to see their wallet address, balance, and optionally their private key.

    :param author: Username of the entity requesting their info
    :param private_info: Whether or not to send the private key (mnemonic) along with the message
    :return:
    """
    helper.praw.redditor(author).message(
        subject="Your " + ("private address and info" if private_info else "public address and balance"),
        message=get_info_as_string(wallet_name=author.lower(), private_info=private_info) + get_signature())
    tipper_logger.log(f'Told {author} their {("private" if private_info else "public")} info.')
