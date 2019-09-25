from tipperInteractions.get_info import *
from tipperInteractions.wallet_generator import *
from tipperInteractions.withdraw import *
from tipperInteractions.tip import *
from helper import *
from decimal import Decimal
from logger import tipper_logger
import re
import json


class MethodHandler(object):
    """
    Handles the different replies and interactions possible with the bot

    :param reddit: The PRAW object to perform on
    """

    reddit = None
    password = None
    botname = None

    below_threshold_message = f"The minimum tip you can send it 1 mXMR, or 0.001 XMR, since that's the minimum I show in the [balance page](https://www.reddit.com/message/compose/?to=MoneroTipsBot&subject=My%20info&message=Hit%20%27send%27%20and%20the%20bot%20will%20tell%20you%20your%20balance%20:\))!"

    def __init__(self, reddit, botname, password="\"\""):
        self.reddit = reddit
        self.password = password
        self.botname = botname

    def get_xmr_val(self, dollars):
        """
        Converts USD to XMR with coingecko API

        :param dollars: dollars in USD
        :return: XMR representing dollar amount
        """
        response = requests.get('https://api.coingecko.com/api/v3/simple/price',
                                headers={'accept': 'application/json'},
                                params=(('ids', 'monero'), ('vs_currencies', 'usd')))

        return float(dollars)/float(json.loads(response.content)["monero"]["usd"])


    def get_tip_recipient(self, comment):
        """
        Determines the recipient of the tip, based on the comment requesting the tip

        :param comment: The comment that notified the bot
        :return: Username of the parent of the comment
        """

        author = None
        try:
            author = comment.parent().author
        except Exception as e:
            tipper_logger.log("Somehow there's no parent at all?")

        return author


    def parse_tip_amount(self, body):
        """
        Tries to parse the amount a Redditor wishes to tip, based on the comment requesting the tip

        :param body: The contents of a comment that called the bot
        :return: An amount, in XMR, that the bot will tip
        """

        m = re.search(f'/u/{self.botname} (tip )?([\\d\\.]+)( )?(m)?xmr', str(body).lower())
        if m:
            return str(Decimal(m.group(2))/1000) if m.group(m.lastindex) == "m" else m.group(2) #Divide by 1000 if mXMR

        m = re.search(f'/u/{self.botname} (tip )?(\\$)?(?P<dollar_amt>[\\d\\.]+)(\\$)?', str(body).lower())
        if m:
            return str(self.get_xmr_val(m.group("dollar_amt")))
        return None


    def parse_withdrawl_amount(self, subject):
        """
        Tries to parse the amount a Redditor wishes to withdraw from their wallet

        :param subject: Subject line in form "Withdraw xyz XMR"
        :return: Ann amount, in XMR, that the bot will withdraw
        """

        m = re.search('withdraw ([\\d\\.]+)( )?(m)?xmr', str(subject).lower())
        if m:
            return str(Decimal(m.group(1))/1000) if m.group(m.lastindex) == "m" else str(Decimal(m.group(1)))

        m = re.search('withdraw (\\$)?(?P<dollar_amt>[\\d\\.]+)(\\$)?', str(subject).lower())
        if m:
            return str(self.get_xmr_val(m.group("dollar_amt")))
        return None


    def handle_tip_request(self, author, body, comment):
        """
        Handles the tipping interaction, called by a Redditor's comment
        Replies to the user if the response is not None
        Sends user a message if message is not None

        :param body: The contents of a comment that called the bot
        :param author: The username of the entity that created the comment
        :param comment: The comment itself that called the bot
        """

        recipient = self.get_tip_recipient(comment)
        amount = self.parse_tip_amount(body)
        reply = None

        if recipient is None or amount is None:
            reply = "Nothing interesting happens.\n\n*In case you were trying to tip, I didn't understand you.*"
        elif Decimal(amount) < 0.001:
            reply = self.below_threshold_message
        else:
            tipper_logger.log(f'{author.name} is sending {recipient} {amount} XMR.')
            generate_wallet_if_doesnt_exist(recipient.name.lower(), self.password)

            res = tip(sender=author.name, recipient=recipient.name, amount=amount, password=self.password)
            if res["response"] is not None:
                reply = f'{res["response"]}'
                tipper_logger.log("The response is: " + reply)
            if res["message"] is not None:
                self.reddit.redditor(author.name).message(subject="Your tip", message=f"Regarding your tip here: {comment.context}\n\n" + res["message"] + signature)

        try:
            if reply is not None:
                self.reddit.comment(str(comment)).reply(reply + signature)
        except Exception as e:
            tipper_logger.log(e)


    def handle_withdraw_request(self, author, subject, contents):
        """
        Handles the withdrawl request, setting up RPC and calling the withdraw function

        :param author: Wallet to withdraw from
        :param subject: The withdrawl request string
        :param contents: The address to withdraw to
        :return: Response message about withdrawl request
        """

        amount = self.parse_withdrawl_amount(subject)
        if amount == None:
            self.reddit.redditor(author.name).message(subject="I didn't understand your withdrawal!", message=f'You sent: "{subject}", but I couldn\'t figure out how much you wanted to send. See [this](https://www.reddit.com/r/MoneroTipsBot/wiki/index#wiki_withdrawing) guide if you need help, or click "Report a Bug" under "Get Started"  if you think there\'s a bug!' + signature)
            return None

        sender_rpc_n_wallet = safe_wallet(port=helper.ports.withdraw_sender_port, wallet_name=author.name.lower(), password=self.password)

        res = handle_withdraw(sender_rpc_n_wallet.wallet, author.name, contents, amount)

        sender_rpc_n_wallet.kill_rpc()

        self.reddit.redditor(author.name).message(subject="Your withdrawl", message=res + signature)
        tipper_logger.log("Told " + author.name + " their withdrawl status (" + res + ")")


    def handle_info_request(self, author, private_info=False):
        """
        Allows Reddit users to see their wallet address, balance, and optionally their private key.

        :param author: Username of the entity requesting their info
        :param private_info: Whether or not to send the private key (mnemonic) along with the message
        :return:
        """
        self.reddit.redditor(author.name).message(subject="Your " + ("private address and info" if private_info else "public address and balance"), message=get_info_as_string(wallet_name=author.name.lower(), private_info=private_info, password=self.password) + signature)
        tipper_logger.log(f'Told {author.name} their {("private" if private_info else "public")} info.')


    def parse_donate_amount(self, subject, senderBalance):
        """
        Parses the amount a user wishes to donate to the CSS based on their message.

        :param subject: Subject line in form "Donate xyz XMR" or "Donate xyz% of my balance"
        :param senderBalance: Their current balance, used to calculate when sending a percentage
        :return: Final amount in XMR they wish to donate
        """

        # "Donate xyz XMR"
        m = re.search('donate ([\\d\\.]+)( )?(m)?xmr', subject.lower())
        if m:
            return str(Decimal(m.group(1))/1000) if m.group(m.lastindex) == "m" else m.group(1)

        # "Donate xyz% of my balance"
        m = re.search('donate ([\\d\\.]+)% of my balance', subject.lower())
        if m:
            return str(float(m.group(1))*float(senderBalance)/100)

        # "Donate xyz$
        m = re.search('donate (\\$)?(?P<dollar_amt>[\\d\\.]+)(\\$)?', str(subject).lower())
        if m:
            return str(self.get_xmr_val(m.group("dollar_amt")))



    def handle_donation(self, author, subject, contents):
        """
        Allows Reddit users to donate a portion of their balance directly to the CCS
        CCS can be seen at: https://ccs.getmonero.org/

        :param author: Reddit account to withdraw from
        :param subject: Subject line of the message, telling how much to withdraw
        :param contents: Message body
        """

        sender_rpc_n_wallet = safe_wallet(port=helper.ports.donation_sender_port, wallet_name=author.name.lower(), password=self.password)

        amount = Decimal(self.parse_donate_amount(subject, sender_rpc_n_wallet.wallet.balance()))

        try:
            generate_transaction(senderWallet=sender_rpc_n_wallet.wallet, recipientAddress=general_fund_address, amount=amount, splitSize=1)
            self.reddit.redditor(author.name).message(subject="Your donation to the General Dev Fund", message=f'Thank you for donating {format_decimal(amount)} of your XMR balance to the CCS!\n\nYou will soon have your total donations broadcasted to the wiki :) {signature}')
            self.reddit.redditor("OsrsNeedsF2P").message(subject=f'{author.name} donated {amount} to the CCS!', message="Update table here: https://old.reddit.com/r/MoneroTipsBot/wiki/index#wiki_donating_to_the_ccs")
            tipper_logger.log(f'{author.name} donated {format_decimal(amount)} to the CCS.')
        except Exception as e:
            self.reddit.redditor(author.name).message(subject="Your donation to the CCS failed", message=f'Please send the following to /u/OsrsNeedsF2P:\n\n' + str(e) + signature)
            tipper_logger.log("Caught an error during a donation to CCS: " + str(e))

        sender_rpc_n_wallet.kill_rpc()


    def parse_anontip_amount(self, subject):
        """
        :param subject: in format "Anonymous tip USER AMOUNT xmr"
        """
        m = re.search('anonymous tip [^ ]+ ([\\d\\.]+)( )?(m)?xmr', subject.lower())
        if m:
            return str(Decimal(m.group(1))/1000) if m.group(m.lastindex) == 'm' else m.group(1)

        m = re.search('anonymous tip [^ ]+ (\\$)?(?P<dollar_amt>[\\d\\.]+)(\\$)?', str(subject).lower())
        if m:
            return str(self.get_xmr_val(m.group("dollar_amt")))


    def parse_anontip_recipient(self, subject):
        """
        :param subject: in format "Anonymous tip USER AMOUNT xmr"
        """
        m = re.search('anonymous tip (.+) .+ (m)?xmr', subject.lower())
        if m:
            generate_wallet_if_doesnt_exist(m.group(1).lower(), self.password)
            if m.group(1) == "automoderator":
                return "monerotipsbot"
            return m.group(1)


    def handle_anonymous_tip(self, author, subject, contents):
        """
        Allows people to send anonymous tips

        :param author: Reddit account to withdraw from
        :param subject: Subject line of the message, telling who to tip and how much
        :param contents: Message body (ignored)
        """

        recipient = self.parse_anontip_recipient(subject)
        amount = self.parse_anontip_amount(subject)

        if recipient is None or amount is None:
            self.reddit.redditor(author.name).message(subject="Your anonymous tip", message="Nothing interesting happens.\n\n*Your recipient or amount wasn't clear to me*" + signature)
            return
        if Decimal(amount) < 0.001: #  Less than amount displayed in balance page
            self.reddit.redditor(author.name).message(subject="Your anonymous tip", message=self.below_threshold_message + signature)
            return

        tipper_logger.log(author.name + " is trying to send " + self.parse_anontip_amount(subject) + " XMR to " + self.parse_anontip_recipient(subject))
        res = tip(sender=author.name, recipient=recipient, amount=amount, password=self.password)
        if res["message"] is not None:
            self.reddit.redditor(author.name).message(subject="Your anonymous tip", message=res["message"] + signature)
        else:
            self.reddit.redditor(author.name).message(subject="Anonymous tip successful",  message=res["response"] + signature)
            recipient_message = signature if contents == "Edit this line to send a message, or leave it exactly the same to attach no message at all!" else "The tipper attached the following message:\n\n" + contents + signature
            self.reddit.redditor(recipient).message("You have recieved an anonymous tip of " + amount + " XMR!", message=recipient_message)
