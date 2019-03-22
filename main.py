from tipperInteractions.tip import *
from tipperInteractions.sendinfo import *
from tipperInteractions.generatewallet import *


def main():
    #tip("testwallet", "testwallet2", 0.6)
    generateWallet("testGeneration")
    print(sendinfo("testGeneration"))



if __name__ == "__main__":
    main()
