from moneroRPC.rpc import RPC
from logger import tipper_logger
import json, requests
import os

def generate_wallet_if_doesnt_exist(name, password):
    """
    Generates a new user wallet, if the user doesn't already have one

    :param name: Name of user generating the wallet
    :return: True if a wallet was generated, False otherwise
    """

    name = str(name)
    if wallet_exists(name):
        print("Wallet exists")
        return False

    return generate_wallet(name=name, password=password)


def wallet_exists(name):
    """

    :param name: Wallet file to look for
    :return: True if found, False otherwise
    """

    print("Checking if wallet exists..")
    name = str(name)
    return os.path.isfile('./wallets/' + name) or os.path.isfile('./wallets/' + name + '.keys') or os.path.isfile('./wallets/' + name + '.address.txt')


def generate_wallet(name, password):
    """
    Generates a new user wallet
    Stores the blockheight in a file named user_blockheight

    :param name: Name of user generating the wallet
    :return True on successful wallet generation, False otherwise
    """

    print("Obviously it doesn't exist")
    name = str(name)
    rpcP = RPC(port=28087, wallet_dir=".", password=password)

    wallet_url = "http://127.0.0.1:28087/json_rpc"
    height_url = "http://127.0.0.1:28081/get_height"
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

    get_blockheight_payload = {
        "jsonrpc" : "2.0",
        "id": "0",
        "method" : "get_height"
    }

    print("Generate_wallet about to call the fun stuff")

    try:
        requests.post(
            wallet_url, data=json.dumps(payload), headers=headers).json()
    except Exception as e:
        tipper_logger.log(e)

    try:
        blockheight_response = requests.post(
            height_url, headers=headers).json()
        print(blockheight_response["height"], file=open('wallets/' + name + ".height", 'w'))
    except Exception as e:
        tipper_logger.log(e)

    rpcP.kill()

    if wallet_exists(name):
        tipper_logger.log("Generated a wallet for " + name)
        return True
    tipper_logger.log("Failed to generate a wallet for " + name)
    return False
