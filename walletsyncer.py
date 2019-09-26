from tipbot.get_info import *
from argparse import ArgumentParser
from logger import tipper_logger
import helper
import traceback
import time
import os, sys


parser = ArgumentParser()
parser.add_argument("-p", "--password", dest="password")
parser.add_argument("-t", "--testnet", dest="testnet")
args = parser.parse_args()


class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

def main():

    try:
        while True:
            for i in os.listdir("wallets/" + ("testnet/" if args.testnet else "mainnet/")):
                if not "." in i:
                    start = int(round(time.time() * 1000))
                    print("Opening " + i + "'s wallet")
                    get_info(i, False, password=args.password, port=helper.ports.wallet_sync_port, timeout=60)
                    if int(round(time.time()*1000))-start > 50000:
                        print("Warn: " + i + "'s wallet is likely unsynced")

    except Exception as e:
        tipper_logger.log("walletsyncer error: " + str(e))
        traceback.print_exc()
        main()



if __name__ == "__main__":
    main()

