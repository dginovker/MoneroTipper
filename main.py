import re

from tipbot.anon_tip import handle_anonymous_tip
from argparse import ArgumentParser
from logger import tipper_logger
import datetime
import praw
import traceback
import helper
from tipbot.backend.wallet_generator import generate_wallet_if_doesnt_exist
from tipbot.donate import handle_donation
from tipbot.get_info import handle_info_request
from tipbot.tip import handle_tip_request
from tipbot.withdraw import handle_withdraw_request


def comment_requests_tip(body):
    return re.search(f'/u/{helper.botname.lower()} (tip )?(\\$)?([\\d\\.]+?)( )?(m)?(xmr)?(\\$)?', str(body).lower())


def process_message(subject, body, author, comment):
    """
    Handles the comment command a user tried to execute

    :param subject: Subject line of private message
    :param body: Body of message
    :param author: Username of author
    :param comment: comment to parse for the command
    """

    tipper_logger.log("Got message " + body)

    tipper_logger.log(f'Received message: {subject} from {author}: {body}')

    generate_wallet_if_doesnt_exist(name=author.lower(), password=args.password)

    if comment_requests_tip(body):
        handle_tip_request(author=author, body=body, comment=comment)
        return
    if subject.lower() in "my info":
        handle_info_request(author=author, private_info=False)
        return
    if subject.lower() in "my private info":
        handle_info_request(author=author, private_info=True)
        return
    if "withdraw" in subject.lower():
        handle_withdraw_request(author=author, subject=subject, contents=body)
        return
    if "donate" in subject.lower():
        handle_donation(author=author, subject=subject)
        return
    if "anonymous tip" in subject.lower():
        handle_anonymous_tip(author=author, subject=subject, contents=body)
        return

    helper.praw.redditor(author).message(subject="I didn't understand your command", message=f'I didn\'t understand what you meant last time you tagged me. You said: \n\n{body}\n\nIf you didn\'t mean to summon me, you\'re all good! If you\'re confused, please let my owner know by clicking Report a Bug!{helper.get_signature()}')


def main():
    tipper_logger.log("Searching for new messages")
    start_time = datetime.datetime.now().timestamp()

    author = None
    try:
        for message in helper.praw.inbox.stream():
            author = message.author.name
            if message.created_utc > start_time:
                process_message(subject=message.subject, body=message.body, author=author, comment=message)
    except Exception as e:
        try:
            if "read timeout" not in str(e).lower() \
                    and "reddit.com timed out" not in str(e) \
                    and "503" not in str(e) \
                    and "Connection aborted" not in str(e) \
                    and "has no attribute 'name'" not in str(e) \
                    or "127.0.0.1" in str(e):  # If localhost is in it, then definitely do send the error msg
                tipper_logger.log("Main error: " + str(e))
                tipper_logger.log("Blame " + author)
                traceback.print_exc()
                helper.praw.redditor(author).message(subject="Something broke!!",
                                                     message="If you tried to do something, please send the following error to /u/OsrsNeedsF2P:\n\n" + str(e) + helper.get_signature())
        except Exception as e:
            tipper_logger.log("Just wow." + str(e))
        main()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-p", "--password", dest="password", default="password", help="Password to Monero wallets")
    parser.add_argument("-a" "--account", dest="account_name", required=True, help="Reddit account username. Must match praw.ini.")
    parser.add_argument("-t", "--testnet", action="store_true", help="Whether to run MoneroTipper on testnet")
    args = parser.parse_args()

    helper.praw = praw.Reddit(args.account_name, user_agent='Monero non-custodial testnet tipper: v0.9 (by /u/OsrsNeedsF2P)')
    helper.botname = helper.praw.user.me().name
    helper.password = args.password

    if args.testnet:
        helper.ports.ports_to_testnet()
        helper.testnet = True

    main()
