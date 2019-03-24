import pprint
import datetime
from tipperInteractions.reply import *
import praw

reddit = praw.Reddit('tipbot', user_agent='Monero non-custodial tipper: v0.1 (by /u/OsrsNeedsF2P)')
replier = ReplyHandler(reddit)


def processMessage(subject, body, author, comment):
    """
    Handles the comment command a user tried to execute

    :param comment: comment to parse for the command
    """

    print("Received message: " + subject + " from " + author.name + ": " + body)

    generate_wallet_if_doesnt_exist(author.name)

    if "/u/monerotipsbot tip" in body.lower():
        replier.handle_tip(author, body, comment)
        return
    if subject == "My info":
        replier.handle_info_request(author=author, private_info=False)
        return
    if subject == "My private info":
        replier.handle_info_request(author=author, private_info=True)
        return
    if "withdraw" in subject.lower():
        replier.handle_withdraw(author=author, subject=subject, contents=body)
        return

    print("Received a message I don't understand: " + author.name + ":\n" + body)


def main():

    print("Searching for new messages")
    startTime = datetime.datetime.now().timestamp()

    for message in reddit.inbox.stream():
        if message.created_utc > startTime:
            #pprint.pprint(vars(message))
            processMessage(subject=message.subject, body=message.body, author=message.author, comment=message)



if __name__ == "__main__":
    main()
