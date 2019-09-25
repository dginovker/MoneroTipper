class BotHandler(object):
    """
    Handles PRAW and different constants

    :param reddit: The PRAW object to perform on
    :param botname: Username of Reddit bot running
    :param wallet_password: Wallet encryption passwords
    """

    reddit = None
    password = None
    botname = None

    below_threshold_message = f"The minimum tip you can send it 1 mXMR, or 0.001 XMR, since that's the minimum I show in the [balance page](https://www.reddit.com/message/compose/?to=MoneroTipsBot&subject=My%20info&message=Hit%20%27send%27%20and%20the%20bot%20will%20tell%20you%20your%20balance%20:\))!"

    def __init__(self, reddit, botname, wallet_password="\"\""):
        self.reddit = reddit
        self.botname = botname
        self.password = wallet_password
