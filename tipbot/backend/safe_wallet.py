import os

from monero.backends.jsonrpc import JSONRPCWallet
from monero.wallet import Wallet

import helper
from logger import tipper_logger
from tipbot.backend.rpc import RPC


class safe_wallet(object):

    wallet = None
    rpc = None

    def __init__(self, port, wallet_name, password=helper.password, timeout=300):
        """
        Creates a monero-python Wallet based on the custom RPC that verifies it was created properly

        :param port: Port to open RPC
        :param password: Password to open the wallet
        :param wallet_name: Lowercase string of username
        :param timeout: How long to let the RPC sync before killing
        """
        self.rpc = RPC(port=port, wallet_name=wallet_name, password=password, load_timeout=timeout)

        if not os.path.isfile("aborted-" + wallet_name):  # Check if wallet was emergency aborted
            self.wallet = Wallet(JSONRPCWallet(port=self.rpc.port, password=self.rpc.password, timeout=self.rpc.load_timeout))
        else:
            tipper_logger.log("WARNING: " + wallet_name + " had their RPC aborted!!!")
            os.remove("aborted-" + wallet_name)

    def kill_rpc(self):
        self.rpc.kill()

