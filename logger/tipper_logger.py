import csv
import datetime


def log(message):
    print(message)
    f = open('logs/general_logs.csv', 'a')
    csv.writer(f).writerow([datetime.datetime.now() ,message])
    f.close()
