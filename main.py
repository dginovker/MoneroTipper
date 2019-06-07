from tipperInteractions.reply import *
from argparse import ArgumentParser
from logger import tipper_logger
import datetime
import praw
import traceback


parser = ArgumentParser()
parser.add_argument("-p", "--password", dest="password")
args = parser.parse_args()

reddit = praw.Reddit('tipbot', user_agent='Monero non-custodial tipper: v0.4 (by /u/OsrsNeedsF2P)')
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

    tipper_logger.log(f'Received message: {subject} from {author.name}: {body}')

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
    if "donate" in subject.lower():
        replier.handle_donation(author=author, subject=subject, contents=body)
        return

    # tipper_logger.log(f'Received message I don\t understand from {author.name}:\n\n {body}')
    reddit.redditor(author.name).message(subject="I didn't understand your command", message=f'I didn\'t understand what you meant [here]({comment.permalink()}). You said: \n\n{body}\n\nIf you didn\'t mean to summon me, you\'re all good! If you\'re confused, please let my owner know by clicking Report a Bug!{signature}')


def main():

    tipper_logger.log("Searching for new messages")
    startTime = datetime.datetime.now().timestamp()

    author = None
    try:
        for message in reddit.inbox.stream():
            author = message.author.name
            if message.created_utc > startTime:
                processMessage(subject=message.subject, body=message.body, author=message.author, comment=message)
    except Exception as e:
        try:
            tipper_logger.log("Main error: " + str(e))
            tipper_logger.log("Blame " + author)
            traceback.print_exc()
            reddit.redditor(author).message(subject="Something broke!!", message="If you tried to do something, please send the following error to /u/OsrsNeedsF2P:\n\n" + str(e))
            author = None
        except Exception as e:
            tipper_logger.log("Just wow." + str(e))
        main()



if __name__ == "__main__":
    main()
