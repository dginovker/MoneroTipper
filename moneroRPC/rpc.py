import shlex, subprocess

class RPC(object):
    """Monero moneroRPC

    Does moneroRPC things?

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

        if walletfile != None:
            command = rpcLocation + " --wallet-file " + walletfile + " --password \"\" --rpc-bind-port " + str(port) + (" --testnet" if testnet else "" ) + (" --disable-rpc" if disableRpcLogin else "")
        else:
            command = rpcLocation + " --wallet-dir " + walletDir + " --rpc-bind-port " + str(port) + (" --testnet" if testnet else "") + (" --disable-rpc-login" if disableRpcLogin else "")

        print(command)
        args = shlex.split(command)

        self.p = subprocess.Popen(args)

    def kill(self):
        """
        Kills the moneroRPC
        """

        self.p.kill()
