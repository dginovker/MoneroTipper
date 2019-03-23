import pprint
import datetime
import re
from tipperInteractions.tip import *
from tipperInteractions.sendinfo import *
from tipperInteractions.generatewallet import *
import praw
import prawcore
import time

reddit = praw.Reddit('tipbot', user_agent='Monero non-custodial tipper: v0.1 (by /u/OsrsNeedsF2P)')


def parseRecipient(body):
    m = re.search('/u/MoneroTipsBot tip (.+?) ', body)
    if m:
        return m.group(1)
    return None


def parseAmount(body):
    m = re.search('/u/MoneroTipsBot tip .+? (.+?)', body)
    if m:
        return m.group(1)
    return None


def processMessage(subject, body, author, comment):
    """
    Handles the comment command a user tried to execute

    :param comment: comment to parse for the command
    """
    #pprint.pprint(vars(author))
    print("Received message: " + subject + " from " + author.name + ": " + body)

    generateWalletIfDoesntExist(author.name)

    if "/u/MoneroTipsBot tip" in body:
        recipient = parseRecipient(body)
        amount = parseAmount(body)
        if recipient != None and amount != None:
            print(author.name + " is sending " + recipient + " " + amount + " XMR.")
            generateWalletIfDoesntExist(recipient)

            res = tip(sender=author.name, recipient=recipient, amount=amount)
            reply = "Response message: " + res["message"] + "\nResponse txid: " + res["txid"]
            try:
                reddit.comment(str(comment)).reply(reply)
            except Exception as e:
                print(e)
            #pprint.pprint(vars(commentID))
            #reddit.submission(commentID).reply(reply)

def main():

    print("Searching for new messages")
    startTime = datetime.datetime.now().timestamp()

    for message in reddit.inbox.stream():
        #pprint.pprint(vars(message))
        if message.created_utc > startTime:
            processMessage(subject=message.subject, body=message.body, author=message.author, comment=message)


#tip("testwallet", "testwallet2", 0.6)
#generateWalletIfDoesntExist("testGeneration5")
#print(sendinfo("testGeneration"))


if __name__ == "__main__":
    main()
