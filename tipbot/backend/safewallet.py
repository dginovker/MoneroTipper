import os

from monero.backends.jsonrpc import JSONRPCWallet
from monero.wallet import Wallet

from helper import password
from logger import tipper_logger
from tipbot.backend.rpc import RPC


class SafeWallet(object):

    wallet = None
    rpc = None
    wallet_password = None
    timeout = None

    def __init__(self, port, wallet_name, wallet_password=password, timeout=300):
        """
        Creates a monero-python Wallet based on the custom RPC that verifies it was created properly

        :param port: Port to open RPC
        :param wallet_password: Password to open the wallet
        :param wallet_name: Lowercase string of username
        :param timeout: How long to let the RPC sync before killing
        """
        self.wallet_password = wallet_password
        self.timeout = timeout

        self.open_rpc(port=port, password=wallet_password, wallet_name=wallet_name, tries=5)



    def open_rpc(self, port, wallet_name, password=wallet_password, timeout=timeout, tries=5):
        if tries == 0:
            tipper_logger.log(f"WARNING: FAILED to open {wallet_name}'s wallet!!")
            return
        self.rpc = RPC(port=port, wallet_name=wallet_name, password=password, load_timeout=timeout)

        if not os.path.isfile("aborted-" + wallet_name):  # Check if wallet was emergency aborted
            self.wallet = Wallet(JSONRPCWallet(port=self.rpc.port, password=self.rpc.password, timeout=self.rpc.load_timeout))
        else:
            tipper_logger.log(f"WARNING: {wallet_name} had their RPC aborted!!! Trying {tries} more times")
            os.remove("aborted-" + wallet_name)
            self.open_rpc(port=port, wallet_name=wallet_name, password=password, timeout=timeout, tries=tries-1)

    def kill_rpc(self):
        self.rpc.kill()

