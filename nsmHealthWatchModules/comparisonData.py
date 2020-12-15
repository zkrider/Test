import ast
from pprint import pprint
import json
import time
import datetime
import traceback
import pandas as pd
from nsmHealthWatchModules.utils import flatten_json


#TODO: It might make the comparisons easier if each section is flattened first

def compareSensorResultsWithTemplateFlat(results):
    """
    TODO: check dospacketforwarding value
    TODO: do we care about packet capture status?


    items that need extra logic:
    applicationidentification to make sure it's set on all ports

    deployddevicesoftware_runningSoftwareVersion needs to find the biggest softwaresReadyForInstallation
    check for values greater than 0 on malwarestatsgroupbyengine_mlawareEngineTrafficStats and malwarestatsgroupbyfile_malwareEngineTrafficStatsByFile_0_fileType
    check for values greater than 0 on advcallbackdetectionstate
    do we care about outbound ssl flows? if ssl is enabled, check:
        outboundsslstats
        sensorsslstats

    DONE - disable/enable checks for ntba/atd/ssl/dxl/epo/gam from config setting

    :param template:
    :param results:
    :return:
    """
    diffs = []

    with open("flatTemplates/sensor.json", "r") as inf:
        template = json.load(inf)
        if results["config"]["externalIntegrations"]["atd"] == 0:
            poppers = []
            keyword = "atd"
            for k in template.keys():
                if keyword in k.lower():
                    print(f"Not checking: {k}")
                    poppers.append(k)
            for p in poppers:
                template.pop(p)

        if results["config"]["externalIntegrations"]["ntba"] == 0:
                poppers = []
                keyword = "ntba"
                for k in template.keys():
                    if keyword in k.lower():
                        print(f"Not checking: {k}")
                        poppers.append(k)
                for p in poppers:
                    template.pop(p)

        if results["config"]["externalIntegrations"]["tie/dxl"] == 0:
                poppers = []
                keyword = "dxl"
                for k in template.keys():
                    if keyword in k.lower():
                        print(f"Not checking: {k}")
                        poppers.append(k)
                for p in poppers:
                    template.pop(p)

        if results["config"]["externalIntegrations"]["outboundssl"] == 0:
            poppers = []
            keyword = "sslstats"
            for k in template.keys():
                if keyword in k.lower():
                    print(f"Not checking: {k}")
                    poppers.append(k)
            for p in poppers:
                template.pop(p)

        if results["config"]["externalIntegrations"]["gam"] == 0:
            poppers = []
            keyword = "gam"
            for k in template.keys():
                if keyword in k.lower():
                    print(f"Not checking: {k}")
                    poppers.append(k)
            for p in poppers:
                template.pop(p)


    # print(template)
    for sensorName, sensorValues in results["sensorData"].items():
        flattenedValues = flatten_json(sensorValues)
        for tk, tv in template.items():
            if tk in flattenedValues.keys():
                fv = flattenedValues[tk]
                if fv != tv:
                    diffs.append(f"sensorData-{sensorName.split(',')[-1]},{tk},{tv},{fv},R")
                else:
                    diffs.append(f"sensorData-{sensorName.split(',')[-1]},{tk},{tv},{fv},G")
            else:
                diffs.append(f"sensorData-{sensorName.split(',')[-1]},{tk} missing from sensorData,-,-,E")

    #TODO: OTHER LOGIC HERE!!!

    return sorted(diffs), template

def compareHealthcheckResultsWithTemplateFlat(results):
    """

    Need to normalize values

    :param results:
    :return:
    """
    with open("flatTemplates/healthcheck.json", "r") as inf:
        template = json.load(inf)
    pass


def comapareManagerResultsWithTemplateFlat(template, flatTemplate, results):
    """
    should count up number of backups files and alert if less than 2
    should check the data of the last backup and it shouldn't be more than 8 days old

    :param template:
    :param flatTemplate:
    :param results:
    :return:
    """

def comapareManagerResultsWithTemplate(template, flatTemplate, results):
    managerDataTemplate = template["managerData"]
    managerDataFlatTemplate = flatTemplate["managerData"]

    numSnortRulesTemplate = int(template["managerData"]["customattackeditor_attackcount"]["snortRulesSupporting_NS_M_VM_SeriesDevicesCurrentCount"])
    numCustomRulesTemplate = int(template["managerData"]["customattackeditor_attackcount"]["customMcAfeeExploitAttacksCurrentCount"])
    currentBackups = results["managerData"]["Maintenance_BackupNow"]["backups"]
    diffs = []

    ### Specific Checks
    # numSnortRules = results["managerData"]["customattackeditor_attackcount"]["snortRulesSupporting_NS_M_VM_SeriesDevicesCurrentCount"]
    # if numSnortRules > numSnortRulesTemplate:
    #     diffs.append(f"Number of Snort Rules over 50% capacity. Currently at {numSnortRules}")
    # numCustomRules = results["managerData"]["customattackeditor_attackcount"]["customMcAfeeExploitAttacksCurrentCount"]
    # if numCustomRules > numCustomRulesTemplate:
    #     diffs.append(f"Number of Custom Rules over 50% capacity. Currently at {numCustomRules}")
    currentBackups = results["managerData"]["Maintenance_BackupNow"]["backups"]
    if len(currentBackups) < 2:
        # diffs.append(f"Number of backups should be greater than 2. Currently at {len(currentBackups)}")
        diffs.append(f"managerData,numberOfBackups,2,{len(currentBackups)}")

    flatResults = {}
    for line in pd.json_normalize(results["managerData"]).transpose().to_csv().splitlines():
        k, v = line.split(",", 1)
        try:
            flatResults[k] = ast.literal_eval(v)
        except:
            flatResults[k] = v

    ft = {}
    for check in managerDataFlatTemplate:
        k, v = check.split(",", 1)
        try:
            ft[k] = ast.literal_eval(v)
        except:
            ft[k] = v
    for k, v in ft.items():
        if k in flatResults.keys():
            if flatResults[k] != v:
                diffs.append(f"managerData,{k},{v},{flatResults[k]},R")
            else:
                diffs.append(f"managerData,{k},{v},{flatResults[k]},G")

    return diffs, managerDataTemplate

def compareDomainResultsWithTemplateFlat(template, flatTemplate, results):
    """
    Need to iterate though all of the domains and run the comparison
    :param template:
    :param flatTemplate:
    :param results:
    :return:
    """
def compareDomainResultsWithTemplate(template, flatTemplate, results):
    #TODO: v2 - better comparison with subdomains, not just domain 0
    ### NOTE: As of 7-14-20, this will only compare domain 0. Subdomains are not supported.
    domainDataTemplate = template["domainData"]
    # print(managerDataTemplate)
    diffs = []

    domains = results["initData"]["domain"]

    for domain in domains:
        domainid, domainName = domain.split(",")
        flatResults = {}
        for line in pd.json_normalize(results["domainData"][domain]).transpose().to_csv().splitlines():
            k, v = line.split(",", 1)
            try:
                flatResults[k] = ast.literal_eval(v)
            except:
                flatResults[k] = v

        ft = {}
        for check in flatTemplate["domainData"]:
            k, v = check.split(",", 1)
            try:
                ft[k] = ast.literal_eval(v)
            except:
                ft[k] = v
        for k, v in ft.items():
            if k in flatResults.keys():
                if flatResults[k] != v:
                    diffs.append(f"domainData-{domainName},{k},{v},{flatResults[k]},R")
                else:
                    diffs.append(f"domainData-{domainName},{k},{v},{flatResults[k]},G")


    return diffs, domainDataTemplate


def comparePolicyResultsWithTemplate(template, flatTemplate, results):
    ###NOTE: this will be hard to implement due to tuning, etc. This may be skipped for the first version
    time.sleep(1)
    policyDataTemplate = template["policies"]
    policyData = results["policies"]["policyDetails"]
    flatPolicyData = pd.json_normalize(policyData).transpose().to_csv().splitlines()
    diffs = ["TBD"]

    propertiesOfInterest = [
        ".properties.protocolsToScan",
        ".scanningOptions",
        ".protectionOptions."
    ]

    temp = {}

    # for line in flatPolicyData:
    #     for prop in propertiesOfInterest:
    #         if prop in line:
    #             print(line)

    # with open("fart.json", "w") as of:
    #     json.dump(policyData, of, indent=8)

    #TODO: trying to pull apart the policy info STOPPED at 7/24/20@0250. as of now, I have the antimalware and inspection policies added to the template, but nothering else
    # pprint(policyData)
    # malwarepolicy = policyData["malwarepolicy"]
    # protectionoptionspolicy = policyData["protectionoptionspolicy"]

    # for policyType, policy in policyData.items():
    #     print(policyType)
    #     print(policy)
        # temp[policyType] = {}
        # for polID, pol in policy.items():
        #     print(polID)
        #     print("pol", pol)
        #     temp[policyType][polID] = pol
            # for line in pd.json_normalize(pol).transpose().to_csv().splitlines():
            #     print(line)
    # pprint(temp)

    # pprint(policyData["policyDetails"])
    # for line in pd.json_normalize(policyData).transpose().to_csv().splitlines():
    #     print(line)

    return diffs, policyDataTemplate

def flattenTemplate(template):
    flatTemplate = {}
    for k, v in template.items():
        # print(k,v)
        # print(k)
        # print(pd.json_normalize(v).transpose().to_csv())
        if "healthcheck" in k: #TODO put in code here for the healthcheck stuff since it's all in fucking lists
            flatTemplate[k] = pd.json_normalize(v).transpose().to_csv().splitlines()
        else:
            flatTemplate[k] = pd.json_normalize(v).transpose().to_csv().splitlines()

    with open("updatedFlatTemplate.json", "w") as of:
        json.dump(flatTemplate, of, indent=8)

def runComparisonWithTemplates(results):
    #TODO need to include the diffs that weren't wrong
    diffsFromTemplate = {}

    # for section, data in results.items():
    #     with open(f"ZZtemporary-flat-{section}.json", "w") as of:
    #         json.dump(flatten_json(data), of, indent=8)

    with open("updatedTemplate.json", "r") as inf:
        template = json.load(inf)

    for section, data in template.items():
        with open(f"flatTemplates/old-{section}.json", "w") as of:
            json.dump(flatten_json(data), of, indent=8)

    exit()

    flatTemplate = flattenTemplate(template)
    del flatTemplate
    with open("updatedFlatTemplate.json", "r") as inf:
        flatTemplate = json.load(inf)



    # with open("specificOutput.json", "r") as inf:
    #     results = json.load(inf)

    ###Compare sensors

    diffsFromTemplate["sensorDiffs"], diffsFromTemplate["sensorBaseline"] = compareSensorResultsWithTemplateFlat(results)
    # diffsFromTemplate["sensorDiffs"], diffsFromTemplate["sensorBaseline"] = compareSensorResultsWithTemplate(template, results)
    #### Compare Health Check
    diffsFromTemplate["healthcheckDiffs"], diffsFromTemplate["healthcheckBaseline"] = compareHealthcheckResultsWithTemplateFlat(results)
    #diffsFromTemplate["healthcheckDiffs"], diffsFromTemplate["healthcheckBaseline"] = compareHealthcheckResultsWithTemplate(template, results)

    return diffsFromTemplate

    ### Compare Manager
    diffsFromTemplate["managerDiffs"], diffsFromTemplate["managerBaseline"] = comapareManagerResultsWithTemplate(template, flatTemplate, results)

    ### Compare Domain
    diffsFromTemplate["domainDiffs"], diffsFromTemplate["domainBaseline"] = compareDomainResultsWithTemplate(template, flatTemplate, results)

    ### Compare Policy
    diffsFromTemplate["policyDiffs"], diffsFromTemplate["PolicyBaseline"] = comparePolicyResultsWithTemplate(template, flatTemplate, results)


    # TODO parse notes section for custom attacks
    # TODO check alert archive sizes
    # TODO last manager installation
    # TODO

    # with open("diffs.json", "w") as of:
    #     json.dump(diffsFromTemplate, of, indent=8)

    return diffsFromTemplate

def runComaprisonWithLastRun():
    # TODO: v2
    pass