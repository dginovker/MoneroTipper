from tipperInteractions.reply import *
from argparse import ArgumentParser
import datetime
import praw


parser = ArgumentParser()
parser.add_argument("-p", "--password", dest="password")
args = parser.parse_args()

reddit = praw.Reddit('tipbot', user_agent='Monero non-custodial tipper: v0.2 (by /u/OsrsNeedsF2P)')
replier = ReplyHandler(reddit=reddit, password=args.password)


def commentRequestsTip(body):
    m = re.search('/u/monerotipsbot (tip )?([\d\.]+?) (t)?xmr', str(body).lower())
    if m:
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
        replier.handle_tip_request(author, body, comment)
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
    reddit.redditor(author.name).message(subject="I didn't understand your command", message="I didn't understand the following: \n\n" + body + "\n\nIf you didn't mean to summon me, you're all good! If you're confused, please let my owner know by clicking Report a Bug!" + signature)


def main():

    print("Searching for new messages")
    startTime = datetime.datetime.now().timestamp()

    try:
        for message in reddit.inbox.stream():
            if message.created_utc > startTime:
                #pprint.pprint(vars(message))
                processMessage(subject=message.subject, body=message.body, author=message.author, comment=message)
    except Exception as e:
        print(e)
        main()



if __name__ == "__main__":
    main()
