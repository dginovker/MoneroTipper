import json
import re

import requests

from tipbot.backend.safewallet import SafeWallet


class Ports:
    monerod_port = 18081
    wallet_sync_port = 18085
    generate_wallet_port = 18086
    get_info_port = 18087
    tip_sender_port = 18088
    tip_recipient_port = 18089
    donation_sender_port = 18090
    withdraw_sender_port = 18091
    create_address_txt_port = 18092

    def ports_to_testnet(self):
        self.monerod_port += 10000
        self.wallet_sync_port += 10000
        self.generate_wallet_port += 10000
        self.get_info_port += 10000
        self.tip_sender_port += 10000
        self.tip_recipient_port += 10000
        self.donation_sender_port += 10000
        self.withdraw_sender_port += 10000
        self.create_address_txt_port += 10000

# Default ports being used by the service
ports = Ports()

# Wallet passwords
password = "password"

# PRAW (Python Reddit API Wrapper) instance
praw = None

# Username of the tipping bot
botname = ""

# True if we're on testnet (different ports, different wallet dir)
testnet = False


### Constants ###
no_message_anon_tip_string = "Edit this line to send a message, or leave it exactly the same to attach no message at all!"

# General dev fund holder address
general_fund_address = '46zarwyDHd8F2GXxVuETVz3wKvEnWic634eYykBS9Q6UbmQfm2y7XRt45KzF6rGT1Pj9YTp55iHRKXZsR7AaxDZM7XqtYRK'

# Number of decimal points to display
precision = 4


### Helper functions ###
def get_signature():
    base = str(f"\n\n*****\n\n")
    emojii = str(f"^\(っ◔◡◔)っ ^♡")
    get_started = str(f" ^| [^(Get Started)](https://old.reddit.com/r/{botname}/wiki/index)")
    show_balance = str(f" ^| [^(Show my balance)](https://www.reddit.com/message/compose/?to={botname}&subject=My%20info&message=Hit%20%27send%27%20and%20the%20bot%20will%20tell%20you%20your%20balance%20:\))")
    donate = str(f" ^| [^(Donate to the CCS)](https://old.reddit.com/r/{botname}/wiki/index#wiki_donating_to_the_ccs)")
    end = str(f" ^| ^♡")
    double_sig = str(f"\n\n ^(NOTICE: This bot is a testnet version. There may be long delays between transactions showing up on the network!)")  if testnet else ""
    return base + emojii + get_started + show_balance + donate + end + double_sig

def get_below_threshold_message():
    return f"The minimum tip you can send it 1 mXMR, or 0.0001 XMR, since that's the minimum I show in the [balance page](https://www.reddit.com/message/compose/?to={botname}&subject=My%20info&message=Hit%20%27send%27%20and%20the%20bot%20will%20tell%20you%20your%20balance%20:\))!"

def get_xmrchain(txid):
    return f"https://{'testnet.' if testnet else ''}xmrchain.com/search?value={str(txid)}"

def format_decimal(decimal, points=precision):
    """
    Formats a decimal number to have the number of decimal points defined to by precision

    :param points: Number of decimal points to add
    :param decimal: Number to format
    :return: Number as a formatted string
    """
    return ("{:." + str(points) + "f}").format(decimal)


def get_xmr_val(dollars):
    """
    Converts USD to XMR with coingecko API

    :param dollars: dollars in USD
    :return: XMR representing dollar amount
    """
    response = requests.get('https://api.coingecko.com/api/v3/simple/price',
                            headers={'accept': 'application/json'},
                            params=(('ids', 'monero'), ('vs_currencies', 'usd')))

    return format_decimal(float(dollars) / float(json.loads(response.content)["monero"]["usd"]))

def is_txid(string):
    return re.search("[0-9a-f]{64}", str(string))


def get_address_txt(wallet_name):
    """
    Gets the address.txt from the wallet without creating a RPC, unless the file doesn't exist, in which case it creates a RPC and saves it

    :param wallet_name: The wallet name to get the address from
    :return: The address
    """
    try:
        return open("wallets/" + ("testnet/" if testnet else "mainnet/") + wallet_name + ".address.txt", "r").read().rstrip()
    except Exception:
        wallet = SafeWallet(port=ports.create_address_txt_port, wallet_name=wallet_name)
        address = wallet.rpc.run_rpc_request('{"jsonrpc":"2.0","id":"0","method":"get_address","params":{"account_index":0,"address_index":[0]}}').json()["result"]["address"]
        print(address, file=open('wallets/' + ("testnet/" if testnet else "mainnet/") + wallet_name + ".address.txt", 'w'))
        wallet.kill_rpc()
        return address

