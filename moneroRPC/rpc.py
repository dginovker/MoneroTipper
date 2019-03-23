import shlex, subprocess

class RPC(object):
    """Monero moneroRPC

    Starts the Monero RPC either for creating or using a wallet file
    wallet dir and wallet files are started in the ./wallets directory

    :param port: the port for the moneroRPC to run on
    """

    port = None
    walletfile = None
    rpcLocation = None
    testnet = None
    walletDir = None
    disableRpcLogin = None
    p = None

    def __init__(self, port, walletfile=None, rpcLocation="../../Programs/monero/monero-wallet-rpc", testnet=True, walletDir=".", disableRpcLogin=True):
        self.port = port
        self.walletfile = walletfile
        self.rpcLocation = rpcLocation
        self.testnet = testnet
        self.walletDir = walletDir
        self.disableRpcLogin = disableRpcLogin

        if walletfile != None: # For opening an existing wallet
            command = rpcLocation + " --wallet-file ./wallets/" + walletfile + " --password \"\" --rpc-bind-port " + str(port) + (" --testnet" if testnet else "" ) + (" --disable-rpc" if disableRpcLogin else "")
        else: # For creating a new wallet
            command = rpcLocation + " --wallet-dir ./wallets/" + walletDir + " --rpc-bind-port " + str(port) + (" --testnet" if testnet else "") + (" --disable-rpc-login" if disableRpcLogin else "")

        print(command)
        args = shlex.split(command)

        self.p = subprocess.Popen(args, stdout=subprocess.PIPE)

    def kill(self):
        """
        Kills the moneroRPC
        """

        self.p.kill()
