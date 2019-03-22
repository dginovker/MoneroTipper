from monero.wallet import Wallet
from monero.backends.jsonrpc import JSONRPCWallet
from monero.seed import Seed
from moneroRPC.rpc import RPC
import time
import json, requests

def generateWallet(name):
    """
    Generates a new user wallet

    :param name: Name of user generating the wallet
    :return True on successful wallet generation, False otherwise
    """

    rpcP = RPC(port=28087)

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
        response = requests.post(
            url, data=json.dumps(payload), headers=headers).json()
        print(response["result"])
        return True
    except:
        return False
