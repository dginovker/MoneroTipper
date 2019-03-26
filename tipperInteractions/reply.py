from tipperInteractions.get_info import *
from tipperInteractions.tip import *
from helper import *
import re


class ReplyHandler(object):
    """
    Handles the different replies and interactions possible with the bot

    :param reddit: The PRAW object to perform on
    """

    reddit = None
    password = None

    def __init__(self, reddit, password="\"\""):
        self.reddit = reddit
        self.password = password


    def get_recipient(self, comment):
        """
        Determines the recipient of the tip, based on the comment requesting the tip

        :param comment: The comment that notified the bot
        :return: Username of the parent of the comment
        """

        author = None
        try:
            author = comment.parent().author
        except Exception as e:
            print("Somehow there's no parent at all?")

        return author


    def parse_tip_amount(self, body):
        """
        Tries to parse the amount a Redditor wishes to tip, based on the comment requesting the tip

        :param body: The contents of a comment that called the bot
        :return: An amount, in XMR, that the bot will tip
        """

        m = re.search('/u/monerotipsbot (tip )?([\d\.]+?) (t)?xmr', str(body).lower())
        if m:
            return m.group(2)
        return None


    def parse_withdrawl_amount(self, subject):
        """
        Tries to parse the amount a Redditor wishes to withdraw from their wallet

        :param subject: The subject line of the withdrawl message
        :return: Ann amount, in XMR, that the bot will withdraw
        """

        m = re.search('withdraw (.+?) xmr', str(subject).lower())
        if m:
            return m.group(1)
        return None


    def handle_tip_request(self, author, body, comment):
        """
        Handles the tipping interaction, called by a Redditor's comment

        :param body: The contents of a comment that called the bot
        :param author: The username of the entity that created the comment
        :param comment: The comment itself that called the bot
        """

        recipient = self.get_recipient(comment)
        amount = self.parse_tip_amount(body)
        reply = None

        if recipient != None and amount != None:
            print(author.name + " is sending " + str(recipient) + " " + amount + " XMR.")
            generate_wallet_if_doesnt_exist(recipient, self.password)

            res = tip(sender=author.name, recipient=recipient, amount=amount, password=self.password)
            reply = "Response message: " + res["response"] + "\n\n[Txid](" + res["txid"] + ")"
            print("The response is: " + reply)
            if res["message"] != None:
                self.reddit.redditor(author.name).message(subject="Your tip", message=res["message"] + signature)
        else:
            reply = "Nothing interesting happens.\n\n*In case you were trying to tip, I didn't understand you.*"

        try:
            self.reddit.comment(str(comment)).reply(reply + signature)
        except Exception as e:
            print(e)


    def handle_withdraw(self, author, subject, contents):
        """
        Handles the withdrawl of Monero to a user's wallet

        :param author: Wallet to withdraw from
        :param subject: The withdrawl request string
        :param contents: The address to withdraw to
        :return: Response message about withdrawl request
        """

        rpcSender = RPC(port=28086, wallet_file=author.name, password=self.password)
        time.sleep(10)

        senderWallet = Wallet(JSONRPCWallet(port=28086, password=self.password))
        amount = self.parse_withdrawl_amount(subject)

        res = None

        if senderWallet.balance(unlocked=True) >= Decimal(amount):
            print(author.name + " is trying to send " + contents + " " + amount + " XMR")
            try:
                res = "Withdrawl success! Txid: "
                res += generate_transaction(senderWallet, contents, Decimal(amount))
            except Exception as e:
                print(e)
                res = "Error: " + str(e)
        else:
            res = "Not enough money to send! Need " + format_decimal(Decimal(amount)) + ", has " + format_decimal(senderWallet.balance(unlocked=True)) + " and " + format_decimal(senderWallet.balance(unlocked=False)) + " still incoming"

        rpcSender.kill()

        self.reddit.redditor(author.name).message(subject="Your withdrawl", message=res + signature)
        print("Told " + author.name + " their withdrawl status (" + res + ")")
        return res


    def handle_info_request(self, author, private_info=False):
        """
        Allows Reddit users to see their wallet address, balance, and optionally their private key.

        :param author: Username of the entity requesting their info
        :param private_info: Whether or not to send the private key (mnemonic) along with the message
        :return:
        """
        self.reddit.redditor(author.name).message(subject="Your " + ("private address and info" if private_info else "public address and balance"), message=get_info(wallet_name=author.name, private_info=private_info, password=self.password) + signature)
        print("Told " + author.name + " their " + ("private" if private_info else "public") + " info.")


