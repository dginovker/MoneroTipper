import shlex, subprocess
import multiprocessing
import time
import os
from datetime import datetime

from logger import tipper_logger




class RPC(object):
    """

    Starts the Monero RPC either for creating or using a wallet file
    wallet dir and wallet files are started in the ./wallets directory

    :param port: Port for the Monero RPC to run on
    :param wallet_name: Wallet name to open on this RPC session
    :param rpc_location: Location on disk where the RPC program sits
    :param testnet: Whether or not to run on the Monero testnet or mainnet
    :param wallet_dir: Directory where all the wallets are kept
    :param disable_rpc_login: Whether or not to use --disable-rpc-login on the RPC
    :param load_timeout: Timeout in seconds for how long to load an RPC
    """
    port = None
    wallet_name = None
    rpc_location = None
    password = None
    testnet = None
    wallet_dir = None
    disable_rpc_login = None
    process = None
    load_timeout = None

    wallet_finished = False
    locked = False

    def __init__(self, port, wallet_name=None, rpc_location="monero/monero-wallet-rpc", password="\"\"", testnet=False, wallet_dir=".", disable_rpc_login=True, load_timeout=300, attempt2=False):
        self.port = port
        self.wallet_name = wallet_name
        self.rpc_location = rpc_location
        self.password = password
        self.testnet = testnet
        self.wallet_dir = wallet_dir
        self.disable_rpc_login = disable_rpc_login
        self.load_timeout = load_timeout

        # For opening an existing wallet
        if wallet_name is not None:
            command = f'{rpc_location} --wallet-file ./wallets/{wallet_name} --password {password} --rpc-bind-port {port}{" --testnet" if testnet else ""}{" --disable-rpc-login" if disable_rpc_login else ""}'

        # For creating a new wallet
        else:
            command = f'{rpc_location} --wallet-dir ./wallets/{wallet_dir} --rpc-bind-port {port}{" --testnet" if testnet else ""}{" --disable-rpc-login" if disable_rpc_login else ""}'

        tipper_logger.log(command)
        args = shlex.split(command)

        self.process = subprocess.Popen(args, stdout=subprocess.PIPE)

        self.waitAndCheckWalletLoad()
        if os.path.isfile("locked") and attempt2 == False:
            print("Wallet locked - waiting 90 sec and trying again")
            os.remove("locked")
            self.kill()
            time.sleep(90)
            self.process = subprocess.Popen(args, stdout=subprocess.PIPE)
            self.waitAndCheckWalletLoad()


    def parseWalletOutput(self):
        if (self.wallet_finished == True):
            return True

        rpc_out = self.process.stdout.readline()
        tipper_logger.log(rpc_out)

        if "starting wallet rpc server" in str(rpc_out.lower()):
            tipper_logger.log("Found out the RPC has started")
            self.wallet_finished = True
        if "error" in str(rpc_out.lower()):
            if "locking fd" in str(rpc_out.lower()):
                tipper_logger.log("The wallet is already open (that's likely fine..)")
                open("locked", "w").close();
            else:
                tipper_logger.log("Found out the RPC has failed")
            self.wallet_finished = True

        return self.wallet_finished

    def isWalletLoaded(self):
        while self.parseWalletOutput() == False:
            time.sleep(0.01)
        tipper_logger.log("Wallet loaded in time")

    def waitAndCheckWalletLoad(self):
        p = multiprocessing.Process(target=self.isWalletLoaded)
        p.start()
        p.join(timeout=self.load_timeout)
        p.kill()
        tipper_logger.log("Killing rpc, hopefully it loaded")


    def kill(self):
        """
        Kills the Monero RPC
        """

        self.process.kill()







