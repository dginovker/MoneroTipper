from wallet_rpc.rpc import RPC
from logger import tipper_logger
import json, requests
import os

import helper

def generate_wallet_if_doesnt_exist(name, password):
    """
    Generates a new user wallet, if the user doesn't already have one

    :param name: Name of user generating the wallet
    :param password: Password for the user wallet
    :return: True if a wallet was generated, False otherwise
    """

    name = str(name)
    if wallet_exists(name):
        return False

    return generate_wallet(name=name, password=password)


def wallet_exists(name):
    """

    :param name: Wallet file to look for
    :return: True if found, False otherwise
    """

    path = "./wallets/" + ("testnet/" if helper.testnet else "mainnet/") + str(name)
    return os.path.isfile(path)


def generate_wallet(name, password):
    """
    Generates a new user wallet
    Stores the blockheight in a file named user_blockheight

    :param name: Name of user generating the wallet
    :return True on successful wallet generation, False otherwise
    """

    name = str(name)
    rpcP = RPC(port=helper.ports.generate_wallet_port, password=password)

    rpc_url = f"http://127.0.0.1:{helper.ports.generate_wallet_port}/json_rpc"
    function_url = "http://127.0.0.1:" + str(helper.ports.generate_wallet_port) + "/get_height"
    headers = {'Content-Type': 'application/json'}

    payload = {
        "jsonrpc" : "2.0",
        "id" : "0",
        "method" : "create_wallet",
        "params": {
            "filename" : name,
            "password" : password,
            "language" : "English",
        }
    }

    try:
        requests.post(
            rpc_url, data=json.dumps(payload), headers=headers).json()
    except Exception as e:
        tipper_logger.log(str(e))

    try:
        blockheight_response = requests.post(
            function_url, headers=headers).json()
        print(blockheight_response["height"] - 10, file=open('wallets/' + ("testnet/" if helper.testnet else "mainnet/") + name + ".height", 'w')) # DON'T CHANGE THIS DUMDUM
    except Exception as e:
        tipper_logger.log(str(e))

    rpcP.kill()

    if wallet_exists(name):
        tipper_logger.log("Generated a wallet for " + name)
        return True
    tipper_logger.log("Failed to generate a wallet for " + name)
    return False
