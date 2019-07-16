from tipperInteractions.get_info import *
from argparse import ArgumentParser
from logger import tipper_logger
import traceback
import time
import os, sys


parser = ArgumentParser()
parser.add_argument("-p", "--password", dest="password")
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
            for i in os.listdir("wallets"):
                if not "." in i:
                    #time.sleep(1)
                    start = int(round(time.time() * 1000))
                    print("Opening " + i + "'s wallet\n\n")
                    get_info(i, False, args.password, port=28444, timeout=20)
                    print("Ran for " + str(int(round(time.time() * 1000)) - start) + " - Closed " + i + "'s wallet\n*************************\n")
            #print("Opening wallet")
            #with HiddenPrints():
            #get_info("OsrsNeedsF2P", False, args.password)
            #print("Closing wallet")

    except Exception as e:
        tipper_logger.log("walletsyncer error: " + str(e))
        traceback.print_exc()
        main()



if __name__ == "__main__":
    main()

