
### Constants ###

# Signature to add to the end of each reply
signature = str("\n\n*****\n\n^\(っ◔◡◔)っ ^♡ ^| [^(Get Started)](https://old.reddit.com/r/MoneroTipsBot/wiki/index) ^| [^(Show my balance)](https://www.reddit.com/message/compose/?to=MoneroTipsBot&subject=My%20info&message=Hit%20%27send%27%20and%20the%20bot%20will%20tell%20you%20your%20balance%20:\)) ^| [^(Donate to the CCS)](https://old.reddit.com/r/MoneroTipsBot/wiki/index#wiki_donating_to_the_ccs) ^| ^♡\n\n ^(NOTICE: Bot is currently in Beta mode for a bit, expect downtime. Back up your seed!)")

# Number of decimal points to display
precision = 4

# General dev fund holder address
general_fund_address = '46zarwyDHd8F2GXxVuETVz3wKvEnWic634eYykBS9Q6UbmQfm2y7XRt45KzF6rGT1Pj9YTp55iHRKXZsR7AaxDZM7XqtYRK'

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


ports = Ports()

# If we are on testnet
testnet = False


# TODO for sometime in the future..
# Add unconfirmed balance function to safe_wallet.py


def format_decimal(decimal, points=precision):
    """
    Formats a decimal number to have the number of decimal points defined to by precision

    :param decimal: Number to format
    :return: Number as a formatted string
    """
    return ("{:." + str(points) + "f}").format(decimal)
