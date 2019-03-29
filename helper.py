
### Constants ###

# Signature to add to the end of each reply
signature = str("\n\n*****\n\n^\(っ◔◡◔)っ ^♡ ^| [^(Deposit)](https://www.reddit.com/message/compose/?to=MoneroTipsBot&subject=My+info&message=Hit+%27send%27+and+the+bot+will+tell+you+your+public+address+:\)) ^| [^(Withdraw)](https://www.reddit.com/message/compose/?to=MoneroTipsBot&subject=Withdraw+0+XMR&message=Replace+this+line+with+your+public+address!) ^|  [^(Show my balance)](https://www.reddit.com/message/compose/?to=MoneroTipsBot&subject=My+info&message=Hit+%27send%27+and+the+bot+will+tell+you+your+balance+:\)) ^| [^(Donate to the CCS)](https://old.reddit.com/r/MoneroTipsBot/wiki/index#wiki_donating_to_the_ccs) ^| [^(Report a bug)](https://old.reddit.com/r/MoneroTipsBot/wiki/index#wiki_report_a_bug) ^| ^♡\n\n^*Testnet ^only")

# Number of decimal points to display
precision = 4

### Default locations ###

logPath = "./logs/"

# TODO for 0.4 release:
# Make "I didn't understand this comment" directly link the comment - Done :)
# Fix withdrawal bug - Done
# Allow for withdrawals directly to the CCS - Partially complete
# Introduce logging
# Make "Main error's" be forwarded to the user
# Fix unconfirmed balance


def format_decimal(decimal):
    """
    Formats a decimal number to have the number of decimal points defined to by precision

    :param decimal: Number to format
    :return: Number as a formatted string
    """
    return ("{:." + str(precision) + "f}").format(decimal)
