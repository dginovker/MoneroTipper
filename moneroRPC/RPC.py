import shlex, subprocess

class RPC(object):
    """Monero moneroRPC

    Does moneroRPC things?

    :param port: the port for the moneroRPC to run on
    """

    port = None
    p = None

    def __init__(self, port):
        self.port = port
        command = "../../Programs/monero/monero-wallet-rpc --testnet --wallet-file testwallet --password \"\" --rpc-bind-port 28088 --disable-rpc-login"
        args = shlex.split(command)

        self.p = subprocess.Popen(args)

    def kill(self):
        """
        Kills the moneroRPC
        """

        self.p.kill()
