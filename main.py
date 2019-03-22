from monero.wallet import Wallet
from monero.backends.jsonrpc import JSONRPCWallet
from moneroRPC.RPC import RPC
import time

start = time.time()


rpcP = RPC(28088)

time.sleep(5)

w = Wallet(JSONRPCWallet(port=28088))

print("It took", time.time() - start, "to get the wallet.")

start = time.time()

print("Address: ", w.address(), "\nHeight: ", w.height(), "\nBalance: ", w.balance())


end = time.time()

print("It has since taken", end - start, " to do all my things")