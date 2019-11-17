from monero import prio
from decimal import Decimal
from logger import tipper_logger
import multiprocessing


def send_sweep_all(sender_wallet, recipient_address, pipe):
    """
    Sends all of the sender's balance to the recipient address

    :param sender_wallet: Wallet to withdraw from
    :param recipient_address: Destination
    :param pipe: Way of returning a string
    """
    pipe.send(str(sender_wallet.sweep_all(recipient_address, priority=prio.UNIMPORTANT)[0][0]))


def broadcast_transaction(sender_wallet, transactions, pipe):
    """
    Sends an array of transactions from sender wallet to recipient
    An array is used to split outputs, allowing better UX for the receiver

    :param sender_wallet: Wallet to send from
    :param transactions: Transactions to send
    :param pipe: Way of returning a string
    """
    pipe.send(str(sender_wallet.transfer_multiple(transactions, priority=prio.UNIMPORTANT)[0].hash))


def timeout_function(target, args, timeout):
    """
    Sets a timeout for a function being run

    :param p: Process to run and timeout
    :param timeout: Time in seconds to wait
    :return: String that the function in process wanted to return
    """
    response = None
    recv_end, send_end = multiprocessing.Pipe(False)
    p = multiprocessing.Process(target=target, args=args+(send_end,))
    p.start()
    p.join(timeout=timeout)
    if not recv_end.poll():
        p.kill()
    else:
        response = recv_end.recv()

    send_end.close()
    recv_end.close()
    return response


def generate_transaction(sender_wallet, recipient_address, amount, split_size=6, timeout=50):
    """
    Generates a transaction with multiple outputs instead of 2
    This allows for the recipient to spend more easily.

    Each output is worth approx. amount/splitSize XMR

    :param sender_wallet: Wallet to send Monero from
    :param recipient_address: Address to receive Monero
    :param amount: The amount to send, in XMR
    :param split_size: The amount of outputs to generate
    :param timeout: Time (in seconds) to try and broadcast a tx before returning failure
    :return: TXID on success, the string "FAILURE" otherwise
    """

    sum = 0
    transactions = []
    if Decimal(amount) < Decimal(0.1) + sender_wallet.balance():
        tipper_logger.log("Sending sweep_all transaction...")

        sweep_res = timeout_function(target=send_sweep_all, args=(sender_wallet, recipient_address), timeout=timeout)

        tipper_logger.log("Sweep res is: " + str(sweep_res))
        if sweep_res == None:
            raise ValueError("The sweep all function timed out! You may have no unlocked balance, or (unlikely) too many inputs!")
        return sweep_res

    # Make multiple of the same output, but in smaller chunks
    for i in range(0, split_size - 1):
        sum += float(amount) / split_size
        transactions.append((recipient_address, Decimal(float(amount) / split_size)))

    # Add the remainder
    transactions.append((recipient_address, Decimal(float(amount) - sum)))

    tipper_logger.log("About to broadcast transaction..")

    broadcast_res =  timeout_function(target=broadcast_transaction, args=(sender_wallet, transactions), timeout=timeout)
    tipper_logger.log("Broadcast res is: " + str(broadcast_res))
    if broadcast_res == None:
        raise ValueError("The broadcast transaction function timed out! You may have too many inputs!")
    return broadcast_res
