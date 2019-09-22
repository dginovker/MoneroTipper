import shlex, subprocess
import multiprocessing
import time
import os
from _signal import SIGTERM

import psutil

from logger import tipper_logger
import helper


class RPC(object):
    """

    Starts the Monero RPC either for creating or using a wallet file
    wallet dir and wallet files are started in the ./wallets directory

    :param port: Port for the Monero RPC to run on
    :param wallet_name: Wallet name to open on this RPC session
    :param rpc_location: Location on disk where the RPC program sits
    :param wallet_dir: Directory where all the wallets are kept
    :param disable_rpc_login: Whether or not to use --disable-rpc-login on the RPC
    :param load_timeout: Timeout in seconds for how long to load an RPC
    """
    port = None
    wallet_name = None
    rpc_location = None
    password = None
    disable_rpc_login = None
    rpc_process = None
    load_timeout = None

    def __init__(self, port, wallet_name=None, rpc_location="monero/monero-wallet-rpc", password="\"\"", disable_rpc_login=True, load_timeout=300):
        self.port = port
        self.wallet_name = wallet_name
        self.rpc_location = rpc_location
        self.password = password
        self.disable_rpc_login = disable_rpc_login
        self.load_timeout = load_timeout

        if wallet_name is not None:  # Open wallet
            rpc_command = f'{rpc_location} --wallet-file ./wallets/{"testnet/" if helper.testnet else "mainnet/"}{wallet_name} --password {password} --rpc-bind-port {port}{" --testnet" if helper.testnet else ""}{" --disable-rpc-login" if disable_rpc_login else ""}'
        else:  # Create new wallet
            rpc_command = f'{rpc_location} --wallet-dir ./wallets/{"testnet/" if helper.testnet else "mainnet/"} --rpc-bind-port {port}{" --testnet" if helper.testnet else ""}{" --disable-rpc-login" if disable_rpc_login else ""}'

        tipper_logger.log(rpc_command)
        rpc_command_shelled = shlex.split(rpc_command)

        self.kill_existing_rpc(port)  # Prevents an old RPC from accidentally being reused
        self.rpc_process = subprocess.Popen(rpc_command_shelled, stdout=subprocess.PIPE)

        self.wait_for_rpc_to_load()
        if os.path.isfile("locked"):  # Check if we were syncing it with walletsyncer.py in another program
            print("Wallet locked - waiting 90 sec and trying again")
            os.remove("locked")
            self.kill()
            time.sleep(90)
            self.rpc_process = subprocess.Popen(rpc_command_shelled, stdout=subprocess.PIPE)
            self.wait_for_rpc_to_load()

    def kill_existing_rpc(self, port):
        for proc in psutil.process_iter():
            try:
                for conns in proc.connections(kind='inet'):
                    if conns.laddr.port == port:
                        proc.send_signal(SIGTERM)
                        print("MURDERING THE SIGNAL")
                        # TODO: Sleep until it's dead, timeout 20 seconds?
            except:
                ""

    def wait_for_rpc_to_load(self):
        """
        Waits for RPC to confirm it's ready for commands
        """
        rpc_read_process = multiprocessing.Process(target=self.check_rpc_loaded)
        rpc_read_process.start()
        rpc_read_process.join(timeout=self.load_timeout)
        rpc_read_process.kill()
        tipper_logger.log("Got final status of rpc reader")

    def check_rpc_loaded(self):
        """
        Loops through RPC output until it detects it's ready/failed
        """
        rpc_output = self.parse_rpc_output()
        while rpc_output == "LOADING":
            time.sleep(0.01)
            rpc_output = self.parse_rpc_output()

        if rpc_output == "FAIL":
            tipper_logger.log("RPC Failed!!! Aborting!")
            self.kill()
            self.kill_existing_rpc(self.port)  # Any wallet attempted to be created with this RPC will now fail
            open("aborted-" + self.wallet_name, "w").close()
            time.sleep(0.01)  # Just in case - time to write

        if rpc_output == "SUCCESS":
            tipper_logger.log("Wallet loaded in time")

    def parse_rpc_output(self):
        """
        Reads 1 line from RPC output
        :return: Status of RPC - LOADING if still unknown, FAIL if an error occurred, SUCCESS otherwise
        """
        rpc_out = self.rpc_process.stdout.readline()
        tipper_logger.log("RPC:" + str(rpc_out))

        if "error" in str(rpc_out).lower() or "failed to initialize" in str(rpc_out).lower():
            if "locking fd" in str(rpc_out.lower()):
                tipper_logger.log("The wallet is already open (that's likely fine..)")
                open("locked", "w").close()
                time.sleep(0.01)  # Just in case
            else:
                tipper_logger.log("Found out the RPC has an error (FAIL)")
            return "FAIL"
        if "starting wallet rpc server" in str(rpc_out.lower()):
            tipper_logger.log("Found out the RPC has started (SUCCESS)")
            return "SUCCESS"

        return "LOADING"

    def kill(self):
        """
        Kills the Monero RPC
        """
        self.rpc_process.kill()
