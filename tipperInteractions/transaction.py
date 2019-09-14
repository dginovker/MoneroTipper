from monero import prio
from decimal import Decimal
from logger import tipper_logger

def generate_transaction(senderWallet, recipientAddress, amount, splitSize=6):
    """
    Generates a transaction with multiple outputs instead of 2
    This allows for the recipient to spend more easily.

    Each output is worth approx. amount/splitSize XMR

    :param senderWallet: Wallet to send Monero from
    :param recipientWallet: Wallet to receive Monero
    :param amount: The amount to send, in XMR
    :param splitSize: The amount of outputs to generate
    :return: RPC return
    """

    sum = 0
    transactions = []
    # Make multiple of the same output, but in smaller chunks
    if senderWallet.balance() - Decimal(amount) < Decimal(0.002):
        tipper_logger.log("Sending sweep_all transaction...")
        temp = str(senderWallet.sweep_all(recipientAddress, priority=prio.UNIMPORTANT)[0][0])
        print("Temp is " + temp)
        return temp

    for i in range(0, splitSize - 1):
        sum += float(amount)/splitSize
        transactions.append((recipientAddress, Decimal(float(amount) / splitSize)))

    # Add the remainder
    transactions.append((recipientAddress, Decimal(float(amount) - sum)))

    tipper_logger.log("About to broadcast transaction..")
    return str(senderWallet.transfer_multiple(transactions, priority=prio.UNIMPORTANT)[0].hash)
