from moneroRPC.rpc import RPC
import time
import json, requests
import os

def generateWalletIfDoesntExist(name):
    """
    Generates a new user wallet, if the user doesn't already have one

    :param name: Name of user generating the wallet
    :return: True if a wallet was generated, False otherwise
    """
    if walletExists(name):
        print("User " + name + " already has a wallet.")
        return False

    return generateWallet(name=name)


def walletExists(name):
    return os.path.isfile('./wallets/' + name) or os.path.isfile('./wallets/' + name + '.keys') or os.path.isfile('./wallets/' + name + '.address.txt')


def generateWallet(name):
    """
    Generates a new user wallet

    :param name: Name of user generating the wallet
    :return True on successful wallet generation, False otherwise
    """

    rpcP = RPC(port=28087, walletDir="./wallets")

    time.sleep(10)

    url = "http://127.0.0.1:28087/json_rpc"
    headers = {'Content-Type': 'application/json'}

    payload = {
        "jsonrpc" : "2.0",
        "id" : "0",
        "method" : "create_wallet",
        "params": {
            "filename" : name,
            "password" : "",
            "language" : "English",
        }
    }

    try:
        requests.post(
            url, data=json.dumps(payload), headers=headers).json()
    except Exception as e:
        print(e)

    if walletExists(name):
        return True
    return False
