import os
import json
import random
import time
from pprint import pprint
import inspect
import datetime
import traceback
from nsmHealthWatchModules import getData
import pandas

def marineCorpsOutput():
    #TODO: needs output to look like:
    # keyname,human readable name, subsection, expected value, actual value 7-16-20@1655
    #TODO: for Marine Corps - 7-16-20@1655
    with open("specificOutputFull.json", "r") as inf:
        results = json.load(inf)

    print("MC")

    diffs = results["templateDiff"]
    allDiffs = []
    diffHeader = "section,check,shouldbe,currentlyis,green/red/exception"
    #TODO: check with tom for the 17 checks we need for MC
    for k, v in diffs.items():
        if "Diffs" in k:
            for diff in v:
                allDiffs.append(diff)

    with open("diffs.txt", "w") as of:
        of.write(diffHeader)
        of.write("\n")
        for d in allDiffs:
            of.write(d)
            of.write("\n")

    mcSpecific = [
        "GetTotalNumberOfAlerts",
        "CheckAlertRate",
        "CheckNumberOfDbConnections",
        "CheckEventTableIndexes",
        "CheckDelayedIncomingAlerts",
        "GetNumberOfPolicies",
        "GetNSMVersion",
        "CheckForSlowQueriesInDatabase",
        "UnusedIPSPolicyCounter",
        "gamupdatesettings",
        "performancemonitoring",
        "advanceddeviceconfiguration",
        "layer7datacollectionStatus",
        "strongPasswordRequired"
    ]
    mcDiffs = []

    for diff in allDiffs:
        for specificItem in mcSpecific:
            if specificItem in diff:
                mcDiffs.append(diff)


    with open("mc.txt", "w") as of:
        of.write(diffHeader)
        of.write("\n")
        for d in mcDiffs:
            of.write(d)
            of.write("\n")

    #TODO logic to convert the "section" and "check" into a more friendly name

    # df = pandas.json_normalize(test).transpose()
    # print(df)

def policystuff(*args, **kwargs):
    results = kwargs["results"]
    def processMalwarePolicy(policy):
        mwp = {"protocols": {}}
        for i in policy["scanningOptions"]:
            # print(i)
            mwp[i["fileType"]] = {}
            mwp[i["fileType"]]["maximumFileSizeScannedInKB"] = i["maximumFileSizeScannedInKB"]
            for engines in i["malwareEngines"]:
                # print(engines)
                if engines["id"] != 8192:
                    mwp[i["fileType"]][engines["name"]] = engines["status"]
        for i in policy["properties"]["protocolsToScan"]:
            mwp["protocols"][i["protocolName"]] = i["enabled"]

        return mwp


    for policyID in results["policies"]["policyDetails"]["malwarepolicy"]:
        policy = results["policies"]["policyDetails"]["malwarepolicy"][policyID]
        mwp = processMalwarePolicy(policy)
        print(policyID)
        print(pandas.json_normalize(mwp).transpose().to_csv())


def pandasStuff(*args, **kwargs):
    results = kwargs["results"]

    for k,v in results.items():
        if type(v) != dict:
            print(k, type(v))
            continue
        print(k)
        try:
            df = pandas.json_normalize(v).transpose()
            print("csv")
            df.to_csv(f"output/{k}.csv")
            print("xlsx")
            df.to_excel(f"output/{k}.xlsx")
            print("html")
            df.to_html(f"output/{k}.html")
            del df
        except:
            traceback.print_exc()

    df = pandas.json_normalize(results).transpose()
    k = "full"
    print("csv")
    df.to_csv(f"output/{k}.csv")
    print("xlsx")
    df.to_excel(f"output/{k}.xlsx")
    print("html")
    df.to_html(f"output/{k}.html")



    # print("csv")
    # df.to_csv("aaaaa.csv")
    # print("xlsx")
    # df.to_excel("aaaaa.xlsx")
    # print("html")
    # df.to_html("aaaaa.html")
