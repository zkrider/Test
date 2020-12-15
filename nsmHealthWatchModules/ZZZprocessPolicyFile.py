import os
import sys
import json
import random
import time
from pprint import pprint
import inspect
import datetime
import traceback
import pandas

def procIPSPolicy():
    print("")

    with open("../response.json", "r") as inf:
        data = json.load(inf)

    # Lists out IPS policy keys from ipspolicies from API
    # for k, v in data["PolicyDescriptor"].items():
    #     if type(v) == dict:
    #         for k2 in v.keys():
    #             if k2 != "TimeStamp":
    #                 print(f"[\"{k}\"][\"{k2}\"]")# = {str(v[k2][0])[:20]}")


    #########GO THOUGH EACH CATEGORY AND COMPARE?
    #########CREATE STATISTICS
    #########GET UNMODIFIED DATAFRAME FROM TESTING FOR COMPARISON
    print("--------------")
    exploitAttacks = data["PolicyDescriptor"]["AttackCategory"]["ExpolitAttackList"]
    exploitAttacksCSV = pandas.json_normalize(exploitAttacks).head().to_csv()
    print(exploitAttacksCSV)
    exploitAttacksCSV = pandas.json_normalize(exploitAttacks).head().transpose().to_csv()
    print(exploitAttacksCSV)


    # for a in exploitAttacks:
    #     print(a)
    #     print(pandas.json_normalize(a))
    print("--------------")
    # exploitAttacksOutbound = data["PolicyDescriptor"]["OutboundAttackCategory"]["ExpolitAttackList"]
    # exploitAttacksOutboundCSV = pandas.json_normalize(exploitAttacksOutbound).to_csv()
    # print(exploitAttacksOutboundCSV)
    # print("--------------")
    # learningAttacks = data["PolicyDescriptor"]["DosPolicy"]["LearningAttack"]
    # learningAttacksCSV = pandas.json_normalize(learningAttacks).to_csv()
    # print(learningAttacksCSV)
    # print("--------------")
    # thresholdAttacks = data["PolicyDescriptor"]["DosPolicy"]["ThresholdAttack"]
    # thresholdAttacksCSV = pandas.json_normalize(thresholdAttacks).to_csv()
    # print(thresholdAttacksCSV)
    # print("--------------")
    # reconAttacks = data["PolicyDescriptor"]["ReconPolicy"]["ReconAttackList"]
    # reconAttacksCSV = pandas.json_normalize(reconAttacks).to_csv()
    # print(reconAttacksCSV)
    # print("--------------")






if __name__ == "__main__":
    procIPSPolicy()


