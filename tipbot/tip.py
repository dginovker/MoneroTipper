import re
import traceback
from decimal import Decimal

import helper
from helper import get_signature
from logger import tipper_logger

from tipbot.backend.transaction import generate_transaction
from tipbot.backend.safewallet import SafeWallet
from tipbot.backend.wallet_generator import generate_wallet_if_doesnt_exist


def get_tip_recipient(comment):
    """
    Determines the recipient of the tip, based on the comment requesting the tip

    :param comment: The PRAW comment that notified the bot
    :return: String representing Username of the parent of the comment
    """

    author = None
    try:
        author = comment.parent().author
    except Exception:
        tipper_logger.log("Somehow there's no parent at all?")

    return fix_automoderator_recipient(author.name)


def handle_tip_request(author, body, comment):
    """
    Handles the tipping interaction, called by a Redditor's comment
    Replies to the user if the response is not None
    Sends user a message if message is not None

    :param body: The contents of a comment that called the bot
    :param author: The username of the entity that created the comment
    :param comment: The comment itself that called the bot
    """

    recipient = get_tip_recipient(comment)
    amount =  helper.parse_amount(f'u/{helper.botname.lower()} (tip )?', body)

    tipper_logger.log(f"Starting tip of {amount} to {recipient}..")

    if recipient is None or amount is None:
        reply = "Nothing interesting happens.\n\n*In case you were trying to tip, I didn't understand you.*"
    elif Decimal(amount) < Decimal(0.0001):
        reply = helper.get_below_threshold_message()
    else:
        tipper_logger.log(f'{author} is sending {recipient} {amount} XMR.')
        generate_wallet_if_doesnt_exist(recipient.lower())

        res = tip(sender=author, recipient=recipient, amount=amount)

        reply = f'{res["response"]}'
        tipper_logger.log("The response is: " + reply)

        if res["message"] is not None:
            helper.praw.redditor(author).message(subject="Your tip", message=f"Regarding your tip here: {comment.context}\n\n" + res["message"] + get_signature())

    helper.praw.comment(str(comment)).reply(reply + get_signature())


def fix_automoderator_recipient(recipient):
    if recipient.lower() == "automoderator":
        tipper_logger.log(f"Changing recipient to {helper.botname} to prevent abuse")
        return helper.botname
    return recipient


def tip(sender, recipient, amount):
    """
    Sends Monero from sender to recipient
    If the sender and the recipient are the same, it creates only 1 rpc
    Always closes RPCs, even on failure

    :param sender: name of wallet sending Monero
    :param recipient: name of wallet receiving
    :param amount: amount to send in XMR
    :return info: dictionary containing txid, a private message and a public response
    """

    info = {
        "txid" : "None",
        "response" : "None", #Comment reply
        "message" : None #Error message
    }

    tipper_logger.log(sender + " is trying to send " + recipient + " " + amount + " XMR")

    sender = str(sender)
    recipient = str(recipient)
    sender_rpc_n_wallet = None

    try:
        sender_rpc_n_wallet = SafeWallet(port=helper.ports.tip_sender_port, wallet_password=helper.password, wallet_name=sender.lower())
        tipper_logger.log("Sender wallet loaded!!")
    except Exception as e:
        sender_rpc_n_wallet.kill_rpc()
        tipper_logger.log("Failed to open wallets for " + sender + " and " + recipient + ". Message: ")
        tipper_logger.log(e)
        info["response"] = "Could not open wallets properly! Perhaps my node is out of sync? (Try again shortly).\n\n^/u/OsrsNeedsF2P!!"
        info["message"] = str(e)
        return info

    tipper_logger.log("Successfully initialized wallets..")

    try:
        recipient_address=helper.get_address_txt(recipient.lower())
        txs = generate_transaction(sender_wallet=sender_rpc_n_wallet.wallet, recipient_address=recipient_address, amount=amount)

        info["txid"] = str(txs)
        info["response"] = f"Successfully tipped /u/{recipient} {amount} XMR! [^(txid)]({helper.get_xmrchain(txs)})"
        tipper_logger.log("Successfully sent tip")
    except Exception as e:
        tipper_logger.log(e)
        traceback.print_exc()
        info["message"] = get_error_response(e)
        info["response"] = "Didn't tip - Check your private message to see why :)"

    sender_rpc_n_wallet.kill_rpc()

    tipper_logger.log("Tip function completed without crashing")

    return info


def get_error_response(e):
    """
    Determines the reply for an exception that occurred when generating a transaction that should have been valid

    :param e: Exception to determine error for
    :return: A reply to be sent publicly to the user regarding the exception
    """
    # Default
    response = "Error: " + str(e)

    if "Method 'transfer_split' failed with RPC Error of unknown code -4" in str(e):  # Not enough spendable inputs
        response = f"Sorry, you do not have enough spendable balance. Wait a bit, or see [this guide](https://www.reddit.com/r/{helper.botname}/wiki/index#wiki_why_is_all_my_monero_unconfirmed.3F_i_want_to_send_more_tips.21) for a solution."
    if "of unknown code -3" in str(e):  # Node out of sync
        response += "\n\n The tipbot node might be really out of sync. Report this to /u/OsrsNeedsF2P"
    if "not enough money" in str(e) or "tx not possible" in str(e):  # Can't afford fee
        response += "\n\n Your balance is either very low (<1 cent) and you cannot cover the network fee, or you're waiting for your return change before you can submit another transaction."
    if "per_subaddress" in str(e):  # No balance, and it tried to run sweep_all
        response += "\n\n You do not have any balance! Try filling some up by clicking \"Get Started\"."

    return response
