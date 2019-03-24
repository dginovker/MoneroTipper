from moneroRPC.rpc import RPC
import time
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
        print("User " + name + " already has a wallet.")
        return False

    return generate_wallet(name=name, password=password)


def wallet_exists(name):
    """

    :param name: Wallet file to look for
    :return: True if found, False otherwise
    """

    name = str(name)
    return os.path.isfile('./wallets/' + name) or os.path.isfile('./wallets/' + name + '.keys') or os.path.isfile('./wallets/' + name + '.address.txt')


def generate_wallet(name, password):
    """
    Generates a new user wallet

    :param name: Name of user generating the wallet
    :return True on successful wallet generation, False otherwise
    """

    name = str(name)
    rpcP = RPC(port=28087, wallet_dir=".", password=password)

    time.sleep(10)

    url = "http://127.0.0.1:28087/json_rpc"
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
            url, data=json.dumps(payload), headers=headers).json()
    except Exception as e:
        print(e)

    rpcP.kill()

    if wallet_exists(name):
        return True
    return False
