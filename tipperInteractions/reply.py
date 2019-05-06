from tipperInteractions.get_info import *
from tipperInteractions.tip import *
from decimal import Decimal
from helper import *
from logger import tipper_logger
import traceback
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
            tipper_logger.log("Somehow there's no parent at all?")

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

        m = re.search('withdraw ([\d\.]+?) (t)?xmr', str(subject).lower())
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

        if recipient is not None and amount is not None:
            tipper_logger.log(f'{author.name} is sending {recipient} {amount} XMR.')
            generate_wallet_if_doesnt_exist(recipient, self.password)

            res = tip(sender=author.name, recipient=recipient.name, amount=amount, password=self.password)
            reply = f'Response message: {res["response"]}\n\n[Txid]({res["txid"]})'
            tipper_logger.log("The response is: " + reply)
            if res["message"] is not None:
                self.reddit.redditor(author.name).message(subject="Your tip", message=res["message"] + signature)
        else:
            reply = "Nothing interesting happens.\n\n*In case you were trying to tip, I didn't understand you.*"

        try:
            self.reddit.comment(str(comment)).reply(reply + signature)
        except Exception as e:
            tipper_logger.log(e)


    def handle_withdraw(self, author, subject, contents):
        """
        Handles the withdrawl of Monero to a user's wallet

        :param author: Wallet to withdraw from
        :param subject: The withdrawl request string
        :param contents: The address to withdraw to
        :return: Response message about withdrawl request
        """

        amount = self.parse_withdrawl_amount(subject)
        if amount == None:
            self.reddit.redditor(author.name).message(subject="I didn't understand your withdrawal!", message=f'You sent: "{subject}", but I couldn\'t figure out how much you wanted to send. See [this](https://www.reddit.com/r/MoneroTipsBot/wiki/index#wiki_withdrawing) guide if you need help, or click "Report a Bug" if you think there\'s a bug!' + signature)
            return None

        rpcSender = RPC(port=28086, wallet_file=author.name, password=self.password)
        time.sleep(10)

        senderWallet = Wallet(JSONRPCWallet(port=28086, password=self.password))

        res = None

        if senderWallet.balance(unlocked=True) >= Decimal(amount):
            tipper_logger.log(f'{author.name} is trying to send {contents} {amount} XMR')
            try:
                res = "Withdrawl success! Txid: "
                res += generate_transaction(senderWallet=senderWallet, recipientAddress=contents, amount=Decimal(amount))
            except Exception as e:
                tipper_logger.log(e)
                res = "Error: " + str(e)
        else:
            walletInfo = get_info(senderWallet)
            res = f'Not enough money to send! Need {format_decimal(Decimal(amount))}, has {walletInfo["balance"]} and {walletInfo["balance_(unconfirmed)"]} still incoming.'

        rpcSender.kill()

        self.reddit.redditor(author.name).message(subject="Your withdrawl", message=res + signature)
        tipper_logger.log("Told " + author.name + " their withdrawl status (" + res + ")")
        return res


    def handle_info_request(self, author, private_info=False):
        """
        Allows Reddit users to see their wallet address, balance, and optionally their private key.

        :param author: Username of the entity requesting their info
        :param private_info: Whether or not to send the private key (mnemonic) along with the message
        :return:
        """
        self.reddit.redditor(author.name).message(subject="Your " + ("private address and info" if private_info else "public address and balance"), message=get_info_as_string(wallet_name=author.name, private_info=private_info, password=self.password) + signature)
        tipper_logger.log(f'Told {author.name} their {("private" if private_info else "public")} info.)')


    def parse_donate_amount(self, subject, senderBalance):
        """
        Parses the amount a user wishes to donate to the CSS based on their message.

        :param subject: Subject line of message being sent
        :param senderBalance: Their current balance, used to calculate when sending a percentage
        :return: Final amount in XMR they wish to donate
        """
        m = re.search('donate (.+) xmr', subject.lower())
        if m:
            return m.group(1)
        m = re.search('donate (.+)% of my balance', subject.lower())
        if m:
            return float(m.group(1))*float(senderBalance)/100


    def handle_donation(self, author, subject, contents):
        """
        Allows Reddit users to donate a portion of their balance directly to the CCS
        CCS can be seen at: https://ccs.getmonero.org/

        :param author: Reddit account to withdraw from
        :param subject: Subject line of the message, telling how much to withdraw
        :param contents: Message body
        :return:
        """

        rpcSender = RPC(port=28090, wallet_file=author.name, password=self.password)
        time.sleep(10)

        senderWallet = Wallet(JSONRPCWallet(port=28090, password=self.password))
        walletInfo = get_info_from_wallet(wallet=senderWallet, private_info=False)

        amount = Decimal(self.parse_donate_amount(subject, senderWallet.balance()))

        if senderWallet.balance(True) < Decimal(amount):
            self.reddit.redditor(author.name).message(subject="Your donation to the CCS", message=f'Unfortunately, you do not have enough funds to donate {format_decimal(amount)} XMR. You have: {walletInfo["balance"]} XMR and {walletInfo["balance_(unconfirmed)"]} + " XMR unconfirmed.')
        else:
            generate_transaction(senderWallet=senderWallet, recipientAddress=general_fund_address, amount=amount, splitSize=1)
            self.reddit.redditor(author.name).message(subject="Your donation to the General Dev Fund", message=f'Thank you for donating {format_decimal(amount)} of your XMR balance to the CCS!\n\nYou will soon have your total donations broadcasted to the wiki :) {signature}')
            self.reddit.redditor("OsrsNeedsF2P").message(subject=f'{author.name} donated {amount} to the CCS!', message="Update table here: https://old.reddit.com/r/MoneroTipsBot/wiki/index#wiki_donating_to_the_ccs")
            tipper_logger.log(f'{author.name} donated {format_decimal(amount)} + " to the CCS.')

        rpcSender.kill()
