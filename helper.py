
### Constants ###

# Signature to add to the end of each reply
signature = str("\n\n*****\n\n^\(っ◔◡◔)っ ^♡ ^| [^(Deposit)](https://www.reddit.com/message/compose/?to=MoneroTipsBot&subject=My+info&message=Hit+%27send%27+and+the+bot+will+tell+you+your+public+address+:\)) ^| [^(Withdraw)](https://www.reddit.com/message/compose/?to=MoneroTipsBot&subject=Withdraw+0+XMR&message=Replace+this+line+with+your+public+address!) ^|  [^(Show my balance)](https://www.reddit.com/message/compose/?to=MoneroTipsBot&subject=My+info&message=Hit+%27send%27+and+the+bot+will+tell+you+your+balance+:\)) ^| [^(Donate to the CCS)](https://old.reddit.com/r/MoneroTipsBot/wiki/index#wiki_donating_to_the_ccs) ^| [^(Report a bug)](https://old.reddit.com/r/MoneroTipsBot/wiki/index#wiki_report_a_bug) ^| ^♡\n\n^*Testnet ^only")

# Number of decimal points to display
precision = 4

# General dev fund holder address
general_fund_address = '9tpz9KzNwpEQyM3yUEGaxSJUWmLqfd9iQRbWB6ndd9qEXVShKhxW4Fif4xQyuwWFYNfji1A9uvjAFDuqYzx9jgWPME8bNRU'

# Port for monerod (currently testnet)
monerod_port = 28081 #18081 for mainet


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


# Mainnet release notes:
# Change monerod port
# Change the CCS donation address to a mainnet address (!!)

def format_decimal(decimal):
    """
    Formats a decimal number to have the number of decimal points defined to by precision

    :param decimal: Number to format
    :return: Number as a formatted string
    """
    return ("{:." + str(precision) + "f}").format(decimal)
