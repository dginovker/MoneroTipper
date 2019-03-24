import shlex, subprocess

class RPC(object):
    """

    Starts the Monero RPC either for creating or using a wallet file
    wallet dir and wallet files are started in the ./wallets directory

    :param port: Port for the Monero RPC to run on
    :param wallet_file: Wallet to open on this RPC session
    :param rpc_location: Location on disk where the RPC program sits
    :param testnet: Whether or not to run on the Monero testnet or mainnet
    :param wallet_dir: Directory where all the wallets are kept
    :param disable_rpc_login: Whether or not to use --disable-rpc-login on the RPC
    """

    port = None
    wallet_file = None
    rpc_location = None
    password = None
    testnet = None
    wallet_dir = None
    disable_rpc_login = None
    process = None

    def __init__(self, port, wallet_file=None, rpc_location="../../Programs/monero/monero-wallet-rpc", password="\"\"", testnet=True, wallet_dir=".", disable_rpc_login=True):
        self.port = port
        self.wallet_file = wallet_file
        self.rpc_location = rpc_location
        self.password = password
        self.testnet = testnet
        self.wallet_dir = wallet_dir
        self.disable_rpc_login = disable_rpc_login

        # For opening an existing wallet
        if wallet_file != None:
            command = rpc_location + " --wallet-file ./wallets/" + wallet_file + " --password " + password + " --rpc-bind-port " + str(port) + (" --testnet" if testnet else "") + (" --disable-rpc" if disable_rpc_login else "")

        # For creating a new wallet
        else:
            command = rpc_location + " --wallet-dir ./wallets/" + wallet_dir + " --rpc-bind-port " + str(port) + (" --testnet" if testnet else "") + (" --disable-rpc-login" if disable_rpc_login else "")

        print(command)
        args = shlex.split(command)

        self.process = subprocess.Popen(args, stdout=subprocess.PIPE)


    def kill(self):
        """
        Kills the Monero RPC
        """

        self.process.kill()
