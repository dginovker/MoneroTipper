import csv
import datetime
import helper

def log(message):
    print(message)
    f = open(f'logs/{"testnet" if helper.testnet else "mainnet"}_general_logs.csv', 'a')
    csv.writer(f).writerow([datetime.datetime.now(), message])
    f.close()
