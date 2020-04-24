from argparse import ArgumentParser
from logger import tipper_logger
import datetime
import praw
import traceback
import helper
from tipbot.parse_message import process_message


def main():
    tipper_logger.log("Searching for new messages")
    start_time = datetime.datetime.now().timestamp()

    author = None
    try:
        for message in helper.praw.inbox.stream():
            if not message.author:
                helper.praw.inbox.mark_read([message]) # Gets rid of messages that otherwise crash service (i.e. sub bans)
            else:
                author = message.author.name
                if message.created_utc > start_time:
                    process_message(author=author, comment=message, subject=message.subject, body=message.body)
    except Exception as e:
        try:
            if "read timeout" not in str(e).lower() \
                    and "reddit.com timed out" not in str(e) \
                    and "503" not in str(e):
                tipper_logger.log("Main error: " + str(e))
                tipper_logger.log("Blame " + author)
                traceback.print_exc()
                helper.praw.redditor("OsrsNeedsF2P").message(subject=f"Something broke for /u/{author}!!",
                                                     message=f"{str(e)}" + helper.get_signature())
        except Exception as e:
            tipper_logger.log("Just wow." + str(e))
        main()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-p", "--password", dest="password", default="password", help="Password to Monero wallets")
    parser.add_argument("-a" "--account", dest="account_name", required=True, help="Reddit account username. Must match praw.ini.")
    parser.add_argument("-t", "--testnet", action="store_true", help="Whether to run MoneroTipper on testnet")
    args = parser.parse_args()

    helper.praw = praw.Reddit(args.account_name, user_agent='Monero non-custodial testnet tipper: v0.11 (by /u/OsrsNeedsF2P)')
    helper.botname = helper.praw.user.me().name
    helper.password = args.password

    if args.testnet:
        helper.ports.ports_to_testnet()
        helper.testnet = True

    main()
