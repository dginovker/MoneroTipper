import json

import requests


class Ports:
    monerod_port = 18081
    wallet_sync_port = 18085
    generate_wallet_port = 18086
    get_info_port = 18087
    tip_sender_port = 18088
    tip_recipient_port = 18089
    donation_sender_port = 18090
    withdraw_sender_port = 18091

    def ports_to_testnet(self):
        self.monerod_port += 10000
        self.wallet_sync_port += 10000
        self.generate_wallet_port += 10000
        self.get_info_port += 10000
        self.tip_sender_port += 10000
        self.tip_recipient_port += 10000
        self.donation_sender_port += 10000
        self.withdraw_sender_port += 10000


# Default ports being used by the service
ports = Ports()

# Wallet passwords
password = ""

# PRAW (Python Reddit API Wrapper) instance
praw = None

# Username of the tipping bot
botname = ""

# True if we're on testnet (different ports, different wallet dir)
testnet = False


### Constants ###
below_threshold_message = f"The minimum tip you can send it 1 mXMR, or 0.001 XMR, since that's the minimum I show in the [balance page](https://www.reddit.com/message/compose/?to=MoneroTipsBot&subject=My%20info&message=Hit%20%27send%27%20and%20the%20bot%20will%20tell%20you%20your%20balance%20:\))!"

no_message_anon_tip_string = "Edit this line to send a message, or leave it exactly the same to attach no message at all!"

# General dev fund holder address
general_fund_address = '46zarwyDHd8F2GXxVuETVz3wKvEnWic634eYykBS9Q6UbmQfm2y7XRt45KzF6rGT1Pj9YTp55iHRKXZsR7AaxDZM7XqtYRK'

# Signature to add to the end of each reply
signature = str("\n\n*****\n\n^\(っ◔◡◔)っ ^♡ ^| [^(Get Started)](https://old.reddit.com/r/MoneroTipsBot/wiki/index) ^| [^(Show my balance)](https://www.reddit.com/message/compose/?to=MoneroTipsBot&subject=My%20info&message=Hit%20%27send%27%20and%20the%20bot%20will%20tell%20you%20your%20balance%20:\)) ^| [^(Donate to the CCS)](https://old.reddit.com/r/MoneroTipsBot/wiki/index#wiki_donating_to_the_ccs) ^| ^♡\n\n ^(NOTICE: Bot is currently in Beta mode for a bit, expect downtime. Back up your seed!)")

# Number of decimal points to display
precision = 4


### Helper functions ###
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

    return float(dollars) / float(json.loads(response.content)["monero"]["usd"])
