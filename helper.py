from decimal import Decimal

signature = str("\n\n*****\n\n^\(っ◔◡◔)っ ^♡ ^| [^(H𝗈𝗐 𝗍𝗈 𝗎𝗌𝖾)](https://www.reddit.com/r/MoneroTipsBot/wiki/index#wiki_how_to_use) ^| [^(𝖥𝖠𝖰)](https://www.reddit.com/r/MoneroTipsBot/wiki/index#wiki_f.a.q.) ^| [^(𝖳𝖾𝗋𝗆𝗌 𝗈𝖿 𝗎𝗌𝖾)](https://www.reddit.com/r/MoneroTipsBot/wiki/index#wiki_terms_of_use) ^| [^(𝖱𝖾𝗉𝗈𝗋𝗍 𝖺 𝖻𝗎𝗀)](https://www.reddit.com/message/compose/?to=OsrsNeedsF2P&subject=/u/MoneroTipsBot%20bug%20report!&message=Please%20be%20as%20detailed%20as%20possible.%20What%20happened?%20What%20should%20have%20happened?%20Thank%20you!) ^| ^♡\n\n^*Testnet ^only")
precision = 4

def format_decimal(decimal):
    """
    Formats a decimal number to have the number of decimal points defined to by precision

    :param decimal: Number to format
    :return: Number as a formatted string
    """
    return ("{:." + str(precision) + "f}").format(decimal)
