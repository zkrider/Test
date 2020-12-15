import os
import json
import random
import time
from pprint import pprint
import inspect
import datetime
import traceback
import pandas
# from nsmHealthWatchModules.getData import getData

def fullHealthcheck(nsmapi):
    startTime = time.time()
    timeOut = 5 * 60
    maxHealthcheckValidAge = 3600 * 24

    def initFullHealthcheck(nsmapi):
        # I can't tell if this is actually running correctly
        url = f"/healthcheck"
        healthcheckData = nsmapi.call(url, method="PUT", message='{"id":["all"]}', verbose=True)

    def getCurrentHealthcheck(nsmapi):
        url = f"/healthcheck"
        healthcheckData = nsmapi.call(url)
        return healthcheckData

    def processHealthcheckData(healthcheckData):
        data = {}
        inprogress = []
        notrun = []
        # pprint(healthcheckData)
        for section in healthcheckData.keys():
            for metric in healthcheckData[section]:
                if metric["notes"] == "In Progress":
                    inprogress.append(metric)
                elif metric["lastRun"] == "":
                    notrun.append(metric)
                elif metric["notes"] != "In Progress":
                    try:
                        deltaT = datetime.datetime.utcnow().timestamp() - time.mktime(time.strptime(metric["lastRun"], "%a %b %d %H:%M:%S %Z %Y"))
                    except:
                        print(metric)
                        traceback.print_exc()
                        deltaT = 99999999
                    data[metric["id"]] = abs(deltaT)
                else:
                    print("unknown state of healthcheck metric", metric)
                    exit()
        return notrun, inprogress, data

    # def flattenHealthcheckData(healthcheckData):
    #     data = {}
    #     for k, v in healthcheckData.items():
    #         data[k] = {}
    #         for v2 in v:
    #             data[k][v2["id"]] = v2
    #
    #     # pprint(data)
    #     return pandas.json_normalize(data).transpose().to_csv()

    runFullHealthCheck = True
    while True:
        healthcheckData = getCurrentHealthcheck(nsmapi)
        notrun, inprogress, data = processHealthcheckData(healthcheckData)
        if inprogress != []:
            print("inprogress", inprogress)
        if notrun != []:
            print("notrun", notrun)
        oldestRun = 0.0
        for k, v in data.items():
            if v >= oldestRun:
                oldestRun = v

        # Checks to make sure timeout hasn't been reached
        if int(time.time() - startTime) > timeOut:
            print("Healthcheck Timeout Reached")
            runFullHealthCheck = False
            break

        # If all checks finish, then break and return
        if len(inprogress) == 0 and len(notrun) == 0 and oldestRun < maxHealthcheckValidAge:
            break

        if oldestRun >= maxHealthcheckValidAge: # If data is outdated, run the full healthcheck
            if runFullHealthCheck:
                initFullHealthcheck(nsmapi)
                runFullHealthCheck = False
            else:
                print(f"Outdated Checks Still In Progress")
        elif len(inprogress) > 0: # If there are "in progress" checks, run the full healthcheck. This does not need a full run check since it's implied there's already something running
            print(f"{len(inprogress)} Checks Still In Progress")
        elif len(notrun) > 0: # If there are healthcheck items that haven't been run
            if runFullHealthCheck:
                initFullHealthcheck(nsmapi)
                runFullHealthCheck = False
            else:
                print(f"{len(inprogress)} items not run, check API call")
        else:
            print("unknown state")
            breakpoint()
        time.sleep(30)

    # flatHealthcheckData = flattenHealthcheckData(healthcheckData)

    return healthcheckData, "" #, flatHealthcheckData



# def runHealthcheckData(nsmapi):
#     url = f"/healthcheck"
#     healthcheckData = nsmapi.call(url, method="PUT", message='{"id":["all"]}')
#
# def checkHealthcheckLastRun(healthcheckData):
#     lastRuns = []
#     for sectionKey, sectionValues in healthcheckData:
#         for metric in sectionValues:
#             lastRun = metric["lastRun"]
#             if None in metric.values():
#                 deltaT = -1
#             elif "progress" in metric["notes"].lower():
#                 deltaT = 0.0
#             else:
#                 try:
#                     deltaT = datetime.datetime.utcnow().timestamp() - time.mktime(time.strptime(lastRun, "%a %b %d %H:%M:%S %Z %Y"))
#                 except:
#                     traceback.print_exc()
#             lastRuns.append((i["lastRun"], deltaT))
#     oldestRun = lastRuns[0]
#     for run in lastRuns:
#         if run[-1] > oldestRun[-1]:
#             oldestRun = run
#
#     return lastRuns, oldestRun
#
# def checkHealthcheckIfInProgress(nsmapi):
#     url = f"/healthcheck"
#     healthcheckData = nsmapi.call(url)
#
#     inProgress = []
#     for section in healthcheckData:
#         for i in healthcheckData[section]:
#             if "progress" in i["notes"].lower():
#                 inProgress.append(i)
#     return inProgress
#
# def getHealthcheckData(results, nsmapi):
#     healthcheckData = {}
#     resource = "healthcheck"
#     url = f"/healthcheck"
#     healthcheckData = nsmapi.call(url)
#     # pprint(healthcheckData)
#
#     lastRuns, oldestRun = checkHealthcheckLastRun(healthcheckData)
#
#     timeOut = time.time()
#     print(oldestRun)
#     if oldestRun[-1] > (60 * 60 * 24) or oldestRun[-1] < -3601:
#         #DONE 5-5-2020
#         if oldestRun[-1] > 0:
#             print("Oldest check was completed over 24 hours ago, rerunning...")
#             inProgress = checkHealthcheckIfInProgress(nsmapi)
#         elif oldestRun[-1] < 0:
#             print("Healthcheck has never been run, running...")
#             inProgress = []
#         if inProgress == []:
#             runHealthcheckData(nsmapi)
#             while True:
#                 inProgress = checkHealthcheckIfInProgress(nsmapi)
#                 if (time.time() - timeOut) > (60 * 5):
#                     print("Timeout waiting for updated healthcheck data, proceeding with current data")
#                     for item in inProgress:
#                         print(f"Waiting on {item['id']}")
#                     break
#                 elif  inProgress == []:
#                     print("No health checks running, continuing...")
#                     break
#                 else:
#                     print(f"Checking for in progress checks...{time.time() - timeOut} elapsed on timeout")
#                     for item in inProgress:
#                         print(f"Waiting on {item['id']}")
#                     time.sleep(30)
#         else:
#             print("checks are still running from the last time this script was run...")
#             pprint(inProgress)
#
#     healthcheckData = nsmapi.call(url)
#
#     return healthcheckData
