import os
import sys
import json
import random
import time
from pprint import pprint
import inspect
import datetime
import traceback
import pickle
import zipfile

def main():

    with zipfile.ZipFile("returnBundle.zip") as inz:
        with inz.open("data.out") as inf:
            pickledData = pickle.load(inf)
        with inz.open("specificOutput.json") as inf:
            specificOutput = json.load(inf)

    if json.dumps(specificOutput) != json.dumps(pickledData):
        for key, pickledDataV in pickledData.items():
            specificOutputV = specificOutput[key]
            sovStr = json.dumps(specificOutputV)
            pdvStr = json.dumps(pickledDataV)
            if pickledDataV != specificOutputV:
                if sovStr != pdvStr:
                    notEqualKey = key
                    print(notEqualKey)
                    print(sovStr == pdvStr)
                    print("sov", len(sovStr), sovStr)
                    print("pdv", len(sovStr), pdvStr)
                    for charPos in range(len(sovStr)):
                        if sovStr[charPos] != pdvStr[charPos]:
                            print(charPos)
    else:
        print("Data Match")

if __name__ == "__main__":
    main()
