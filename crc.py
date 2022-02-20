import random
import time, os
from datetime import datetime, date

#code translated from js

#right shift without sign extension
def rshift(val, n): 
    return val >> n if val >= 0 else (val+0x100000000)>>n

def getCRCTable():
    signedTxHex = 0
    signedTransactions = []
    signedTransactionsCounter = 0
    
    for signedTransactionsCounter in range(256):
        signedTxHex = signedTransactionsCounter

        tmp = 0
        for tmp in range(8):
            signedTxHex = 3988292384 ^ rshift(signedTxHex, 1) \
                          if signedTxHex & 1 \
                          else rshift(signedTxHex, 1)

        signedTransactions.append(signedTxHex)
    
    return signedTransactions

def crc(param):
    crcTable = getCRCTable()

    crc = 0 ^ -1

    for i in range(len(param)):
        index = (crc ^ ord(param[i])) & 255
        crc = rshift(crc, 8) ^ crcTable[index]

    return rshift((crc ^ -1), 0)

def api():
    return "public-api"

def uuidv4():
    mask = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"
    dialog_id = ""
    for ch in mask:
        if ch == 'x' or ch == 'y':
            r = int(random.random() * 16) | 0
            v = r if ch == 'x' else r & 3 | 8
            dialog_id += format(v,'x')
        else:
            dialog_id += ch

    return dialog_id



def getCRCSign(t):
    return crc(f"{api()}{t}qVxRWnespIsJg7DxFbF6N9FiQR5cjnHyygru3JcToH4dPdiNH5SXOYIc00qMXPKJ")

def unix_time():
    os.environ['TZ'] = 'Europe/Moscow'
    time.tzset()

    dt = datetime.today()
    epoch = datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds() * 1000 - 10**7

