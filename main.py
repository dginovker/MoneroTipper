import pprint
import datetime
from tipperInteractions.reply import *
import praw
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument("-p", "--password", dest="password")
args = parser.parse_args()

reddit = praw.Reddit('tipbot', user_agent='Monero non-custodial tipper: v0.1 (by /u/OsrsNeedsF2P)')
replier = ReplyHandler(reddit=reddit, password=args.password)


def commentRequestsTip(body):
    m = re.search('/u/monerotipsbot (tip )?([\d\.]+?) xmr', str(body).lower())
    if m:
        if m.lastindex == 2:
            return True
    return False


def processMessage(subject, body, author, comment):
    """
    Handles the comment command a user tried to execute

    :param comment: comment to parse for the command
    """

    print("Received message: " + subject + " from " + author.name + ": " + body)

    generate_wallet_if_doesnt_exist(name=author.name, password=args.password)

    if commentRequestsTip(body):
        replier.handle_tip(author, body, comment)
        return
    if subject.lower() in "my info":
        replier.handle_info_request(author=author, private_info=False)
        return
    if subject.lower() in "my private info":
        replier.handle_info_request(author=author, private_info=True)
        return
    if "withdraw" in subject.lower():
        replier.handle_withdraw(author=author, subject=subject, contents=body)
        return

    print("Received a message I don't understand: " + author.name + ":\n" + body)
    reddit.redditor(author.name).message(subject="I didn't understand your command", message="I didn't understand the following: \n\n" + body + "\n\nIf you're confused, please let my owner know by clicking Report a Bug!" + signature)


def main():

    print("Searching for new messages")
    startTime = datetime.datetime.now().timestamp()

    for message in reddit.inbox.stream():
        if message.created_utc > startTime:
            #pprint.pprint(vars(message))
            processMessage(subject=message.subject, body=message.body, author=message.author, comment=message)



if __name__ == "__main__":
    main()
