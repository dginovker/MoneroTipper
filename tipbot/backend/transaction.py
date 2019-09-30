from monero import prio
from decimal import Decimal
from logger import tipper_logger


def generate_transaction(sender_wallet, recipient_address, amount, split_size=6):
    """
    Generates a transaction with multiple outputs instead of 2
    This allows for the recipient to spend more easily.

    Each output is worth approx. amount/splitSize XMR

    :param sender_wallet: Wallet to send Monero from
    :param recipient_address: Address to receive Monero
    :param amount: The amount to send, in XMR
    :param split_size: The amount of outputs to generate
    :return: RPC return
    """

    sum = 0
    transactions = []
    if sender_wallet.balance() - Decimal(amount) < Decimal(0.002):
        tipper_logger.log("Sending sweep_all transaction...")
        sweep_all_res = str(sender_wallet.sweep_all(recipient_address, priority=prio.UNIMPORTANT)[0][0])
        print("sweep_all_res is " + sweep_all_res)
        return sweep_all_res

    # Make multiple of the same output, but in smaller chunks
    for i in range(0, split_size - 1):
        sum += float(amount) / split_size
        transactions.append((recipient_address, Decimal(float(amount) / split_size)))

    # Add the remainder
    transactions.append((recipient_address, Decimal(float(amount) - sum)))

    tipper_logger.log("About to broadcast transaction..")
    return str(sender_wallet.transfer_multiple(transactions, priority=prio.UNIMPORTANT)[0].hash)
