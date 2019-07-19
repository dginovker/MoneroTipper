
### Constants ###

# Signature to add to the end of each reply
signature = str("\n\n*****\n\n^\(っ◔◡◔)っ ^♡ ^| [^(Get Started)](https://www.reddit.com/message/compose/?to=MoneroTipsBot&subject=My%20info&message=Hit%20%27send%27%20and%20the%20bot%20will%20tell%20you%20your%20balance) ^| [^(Withdraw)](https://www.reddit.com/message/compose/?to=MoneroTipsBot&subject=Withdraw%200%20XMR&message=Replace%20this%20line%20with%20your%20public%20address!) ^| [^(Donate to the CCS)](https://old.reddit.com/r/MoneroTipsBot/wiki/index#wiki_donating_to_the_ccs) ^| ^♡")
#signature = str("\n\n*****\n\n^\(っ◔◡◔)っ ^♡ ^| [^(Deposit)](https://www.reddit.com/message/compose/?to=MoneroTipsBot&subject=My%20info&message=Hit%20%27send%27%20and%20the%20bot%20will%20tell%20you%20your%20public%20address) ^| [^(Withdraw)](https://www.reddit.com/message/compose/?to=MoneroTipsBot&subject=Withdraw%200%20XMR&message=Replace%20this%20line%20with%20your%20public%20address!) ^|  [^(Show my balance)](https://www.reddit.com/message/compose/?to=MoneroTipsBot&subject=My%20info&message=Hit%20%27send%27%20and%20the%20bot%20will%20tell%20you%20your%20balance) ^| [^(Donate to the CCS)](https://old.reddit.com/r/MoneroTipsBot/wiki/index#wiki_donating_to_the_ccs) ^| [^(Report a bug)](https://old.reddit.com/r/MoneroTipsBot/wiki/index#wiki_report_a_bug) ^| ^♡\n\n^*Mainnet ^(*Make sure you own your private key!)")

# Number of decimal points to display
precision = 4

# General dev fund holder address
general_fund_address = '46zarwyDHd8F2GXxVuETVz3wKvEnWic634eYykBS9Q6UbmQfm2y7XRt45KzF6rGT1Pj9YTp55iHRKXZsR7AaxDZM7XqtYRK'

# Port for monerod (currently testnet)
monerod_port = 18081 #18081 for mainet


# TODO for 0.4 release:
# Make "I didn't understand this comment" directly link the comment - Done :)
# Fix withdrawal bug - Done
# Allow for withdrawals directly to the CCS - Done
# Introduce logging - Done
# Make "Main error's" be forwarded to the user - Done
# Fix unconfirmed balance - API issue?

# TODO for 0.5 release:
# Make RPC loading more efficient - Done :)

# TODO for 0.6 release:
# Restore height is now part of the private info - Done
# Add .gitignore to the repo - Done
# Test testnet from commandline server

# TODO for sometime in the future..
# Tips break return change as well
# Private donations
# Withdrawls dm tx private key
# Add withdrawal address verification https://github.com/0x9090/CrypocurrencyAddressValidation
# QR code for your public address


# Mainnet release notes:
# Change monerod port
# Change the CCS donation address to a mainnet address (!!)

def format_decimal(decimal, points=precision):
    """
    Formats a decimal number to have the number of decimal points defined to by precision

    :param decimal: Number to format
    :return: Number as a formatted string
    """
    return ("{:." + str(points) + "f}").format(decimal)
