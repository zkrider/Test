import os
import json
import random
import time
from pprint import pprint
import inspect
import datetime
import traceback


def compareSensorResultsWithTemplate(template, results):
    sensorDataTemplate = template["sensorData"]
    # print(sensorDataTemplate)
    diffs = []
    #TODO: move to a dict from a list
    keysRequiringExtraProcessing = [
        "deployddevicesoftware-softwaresReadyForInstallation",
        "ipsettings-ipv4Parameter",
        "ipsettings-ipv6Parameter",
        "layer7datacollectionStatus-flows",
        "layer7datacollectionStatus-protocols",
        "passivedeviceprofiling-passiveDeviceProfilingSetting",
        "sensorUpdateInfo-pendingChanges",
        "statelessScanningException-tcpRules",
        "statelessScanningException-udpRules",
        "statelessScanningException-vlanRules",
        "tcpsettings-tcpParameter",
    ]

    for sensor, sensorData in results["sensorData"].items():
        print(f"Checking differences with {sensor}")
        for templateKey, templateValue in sensorDataTemplate.items():
            try:
                if type(sensorData[templateKey]) == dict:
                    #TODO: unpack the fucking dict
                    keys = sensorData[templateKey].keys()
                    if "errorMessage" in keys or "errorId" in keys:
                        diffs.append(f"sensorData-{sensor.split(',')[-1]},{templateKey},{sensorData[templateKey]},E,E")
                        continue
                    for tk, tv in templateValue.items():
                        templateKeytk = f"{templateKey}-{tk}"
                        if templateKeytk in keysRequiringExtraProcessing:
                            print(templateKeytk)
                            print("need to figure out what to do with this...")
                            # flattv = pd.json_normalize(tv).transpose().to_csv().splitlines()[1:]
                            # pprint(flattv)

                        if sensorData[templateKey][tk] != tv:
                            # print(templateKey, tk, sensorData[templateKey][tk], tv)
                            diffs.append(f"sensorData-{sensor.split(',')[-1]},{templateKey}-{tk},{sensorData[templateKey][tk]},{tv},R")
                        else:
                            diffs.append(f"sensorData-{sensor.split(',')[-1]},{templateKey}-{tk},{sensorData[templateKey][tk]},{tv},G")
                elif type(sensorData[templateKey]) == str:
                    if sensorData[templateKey] != templateValue:
                        diffs.append(f"sensorData-{sensor.split(',')[-1]},{templateKey},{sensorData[templateKey]},{templateValue},R")
                    else:
                        diffs.append(f"sensorData-{sensor.split(',')[-1]},{templateKey},{sensorData[templateKey]},{templateValue},G")
                elif type(sensorData[templateKey]) == list:
                    if sensorData[templateKey] != templateValue:
                        diffs.append(f"sensorData-{sensor.split(',')[-1]},{templateKey},{sensorData[templateKey]},{templateValue},R")
                    else:
                        diffs.append(f"sensorData-{sensor.split(',')[-1]},{templateKey},{sensorData[templateKey]},{templateValue},G")
            except:
                diffs.append(f"sensorData-{sensor.split(',')[-1]}-exception,{templateKey},{traceback.format_exc()},E,E")
                breakpoint()

    for item in results["healthcheck"]["summary"]:
        if item["id"] == "GetNSMVersion":
            nsmMajorRev = ".".join(item["result"].split(".")[:2])

    for sensor, sensorData in results["sensorData"].items():
        try:
            versionsAvail = sensorData["deployddevicesoftware"]["softwaresReadyForInstallation"]
            latestAvailableOnManager = sorted(versionsAvail)[0]
            #TODO: include in versions file a "shuould be running" version
            current = sensorData["deployddevicesoftware"]["runningSoftwareVersion"]
            latestGA = results["versions"]["sensorVersions"][results["versions"]["nsmMajorRevision"]][sensorData["model"]]
            if latestAvailableOnManager != current:
                diffs.append(f"sensorData-{sensor.split(',')[-1]},sensorVersionAvailable,{current},{latestAvailableOnManager},R")
            else:
                diffs.append(f"sensorData-{sensor.split(',')[-1]},sensorVersionAvailable,{current},{latestAvailableOnManager},G")
            if latestAvailableOnManager != latestGA:
                diffs.append(f"sensorData-{sensor.split(',')[-1]},sensorVersionGA,{latestAvailableOnManager},{latestGA},R")
            else:
                diffs.append(f"sensorData-{sensor.split(',')[-1]},sensorVersionGA,{latestAvailableOnManager},{latestGA},G")
        except:
            diffs.append(f"sensorData-{sensor.split(',')[-1]}-exception,sensorVersion,{sensorData['deployddevicesoftware']},E,E")

    # for line in diffs:
    #     print(line)

    return sorted(diffs), sensorDataTemplate

def compareHealthcheckResultsWithTemplate(template, results):
    # done 5-5-2020
    healthcheckTemplate = template["healthcheck"]
    diffs = []
    healthcheckResultsFlat = {}
    healthcheckTemplateFlat = {}

    for cat, subcats in results["healthcheck"].items():
        for subcat in subcats:
            healthcheckResultsFlat[subcat["id"]] = subcat

    for cat, subcats in healthcheckTemplate.items():
        for subcat in subcats:
            healthcheckTemplateFlat[subcat["id"]] = subcat

    ### Specific for LastManagerInstallationUpgradeResults
    for check in healthcheckResultsFlat["LastManagerInstallationUpgradeResults"]["notes"].split("\n"):
        num, typeOfRes = check.split(" ")
        if typeOfRes != "Successes" and int(num) > 0:
            diffs.append(f"healthcheck,LastManagerInstallationUpgradeResults,0 {typeOfRes},{check},R")
        else:
            diffs.append(f"healthcheck,LastManagerInstallationUpgradeResults,0 {typeOfRes},{check},G")

    ### Specific for GetNSMLastRebootTimeEpoch
    dateTimeGetNSMLastRebootTime = datetime.datetime.strptime(healthcheckResultsFlat["GetNSMLastRebootTime"]["result"], "%b %d %H:%M:%S %Y")
    deltaTdateTimeGetNSMLastRebootTime = str(datetime.datetime.now() - dateTimeGetNSMLastRebootTime)
    timeGetNSMLastRebootTimeEpoch = time.mktime(time.strptime(healthcheckResultsFlat["GetNSMLastRebootTime"]["result"], "%b %d %H:%M:%S %Y"))
    deltaTGetNSMLastRebootTimeEpoch = time.time() - timeGetNSMLastRebootTimeEpoch

    if (deltaTGetNSMLastRebootTimeEpoch) > (60 * 60 * 24 * 30):
        diffs.append(f"healthcheck,GetNSMLastRebootTime,{deltaTdateTimeGetNSMLastRebootTime.replace(',', '')},<30 days,R")
    else:
        diffs.append(f"healthcheck,GetNSMLastRebootTime,{deltaTdateTimeGetNSMLastRebootTime.replace(',', '')},<30 days,G")

    ### Specific for LastDatabaseBackup
    dateTimeLastDatabaseBackup = datetime.datetime.strptime(healthcheckResultsFlat["LastDatabaseBackup"]["result"], "%b %d %H:%M:%S %Y")
    deltaTdateTimeLastDatabaseBackup = str(datetime.datetime.now() - dateTimeLastDatabaseBackup)
    timeLastDatabaseBackupEpoch = time.mktime(time.strptime(healthcheckResultsFlat["LastDatabaseBackup"]["result"], "%b %d %H:%M:%S %Y"))
    deltaTLastDatabaseBackupEpoch = time.time() - timeLastDatabaseBackupEpoch

    if (deltaTLastDatabaseBackupEpoch) > (60 * 60 * 24 * 30):
        diffs.append(f"healthcheck,LastDatabaseBackup,{deltaTdateTimeLastDatabaseBackup.replace(',', '')},<30 days,R")
    else:
        diffs.append(f"healthcheck,LastDatabaseBackup,{deltaTdateTimeLastDatabaseBackup.replace(',', '')},<30 days,G")

    acceptableOperands = ["<", ">", "="]

    def normalizeDataSize(origvalue):
        # check for file or data sizes and normalize
        fineTypeButShouldntNormalize = [
            "man.man.man.man",
            "sig.sig.sig.sig",
            "bot.bot.bot.bot",
            "Pass",
            "Fail",
            None,
            "None"
        ]
        normvalue = origvalue
        try:
            normvalue = ast.literal_eval(origvalue)
        except:
            try:
                if origvalue == "":
                    pass
                elif origvalue in fineTypeButShouldntNormalize:
                    pass
                    # TODO: throw a warning here for having man.man.man.man or sig.sig.sig.sig

                elif origvalue[-2:] in ["KB", "MB", "GB", "TB"]:
                    value, unit = origvalue.split(" ")

                    if unit == "KB":
                        normvalue = float(value) * 1024
                    elif unit == "MB":
                        normvalue = float(value) * 1024 * 1024
                    elif unit == "GB":
                        normvalue = float(value) * 1024 * 1024 * 1024
                    elif unit == "TB":
                        normvalue = float(value) * 1024 * 1024 * 1024 * 1024
                elif "%" == origvalue[-1]:
                    normvalue = float(origvalue[:-1])
                elif "/sec" in origvalue:
                    if " " in origvalue:
                        normvalue = float(origvalue.split(" ")[0])
                    elif origvalue.split("/")[0].isdigit() or origvalue.split("/")[0].isdecimal():
                        normvalue = float(origvalue.split("/")[0])
                    else:
                        normvalue = float(origvalue.split("/sec")[0])
                elif "ms" == origvalue[-2:]:
                    normvalue = float(origvalue.split("ms")[0])
                elif "," in origvalue:
                    normvalue = origvalue.replace(",", "")
                else:
                    print(f"unk: {origvalue}")
            except:
                print(f"unknown type: {origvalue}")

            try:
                normvalue = float(normvalue)
            except:
                pass

            if normvalue == None:
                pass
            elif type(normvalue) == float or type(normvalue) == int:
                pass
            elif str(normvalue).count(".") == 3:
                pass
            elif normvalue.isdecimal():
                pass
            elif normvalue.isdigit():
                pass
            elif normvalue == "":
                pass
            elif normvalue == "Pass" or normvalue == "Fail":
                pass
            else:
                print("may not need normalization:", origvalue, normvalue)

        return origvalue, normvalue

    for templateK, templateV in healthcheckTemplateFlat.items():
        #TODO: Precheck for Nonetypes and add as errors

        operand = templateV["result"][0]
        origtemplateValue, templateValue = normalizeDataSize(templateV["result"][1:])
        orighealthcheckValue, healthcheckValue = normalizeDataSize(healthcheckResultsFlat[templateK]["result"])
        try:
            if operand not in acceptableOperands:
                print("missing operand")
                print(templateV)
            elif operand == "=":
                if healthcheckValue != templateValue:
                    # print(healthcheckValue, operand, templateValue)
                    diffs.append(f"healthcheck,{templateK},{orighealthcheckValue},{templateV['result']},R")
                else:
                    diffs.append(f"healthcheck,{templateK},{orighealthcheckValue},{templateV['result']},G")
            elif operand == ">":
                if healthcheckValue <= templateValue:
                    # print(healthcheckValue, operand, templateValue)
                    diffs.append(f"healthcheck,{templateK},{orighealthcheckValue},{templateV['result']},R")
                else:
                    diffs.append(f"healthcheck,{templateK},{orighealthcheckValue},{templateV['result']},G")
            elif operand == "<":
                if healthcheckValue >= templateValue:
                    # print(healthcheckValue, operand, templateValue)
                    diffs.append(f"healthcheck,{templateK},{orighealthcheckValue},{templateV['result']},R")
                else:
                    diffs.append(f"healthcheck,{templateK},{orighealthcheckValue},{templateV['result']},G")
            else:
                print("missing operand")
                print(templateV)
        except:
            if results["config"]["DEBUG"]:
                traceback.print_exc()
            #TODO check for Nonetypes and mismatched datatypes
            diffs.append(f"healthcheck-exception,{templateK},{orighealthcheckValue},{templateV['result']},E")

        # for subcatK, subcatV in subcat.items():
        #     print(subcatK, subcatV)
        #
        # for templateKey, templateValue in sensorDataTemplate.items():
        #     if type(sensorData[templateKey]) == dict:
        #         for tk, tv in templateValue.items():
        #             if sensorData[templateKey][tk] != tv:
        #                 # print(templateKey, tk, sensorData[templateKey][tk], tv)
        #                 diffs.append(
        #                     f"{sensor.split(',')[-1]},{templateKey}-{tk},{sensorData[templateKey][tk]},{tv}")

    # print(diffs)
    return diffs, healthcheckTemplateFlat
