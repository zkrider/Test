import pickle
import sys
import re
import os
import json
import random
import time
from pprint import pprint
import inspect
import datetime
import traceback
import api
import tempfile
#from specificOutput import specificOutput
from nsmHealthWatchModules.fileGenerators import generateCredentialsFile
from nsmHealthWatchModules.policyData import getPolicyAssignments
from nsmHealthWatchModules.getData import getData
from nsmHealthWatchModules.sensorData import getSensorData
# from nsmHealthWatchModules.healthcheckData import checkHealthcheckIfInProgress
# from nsmHealthWatchModules.healthcheckData import checkHealthcheckLastRun
# from nsmHealthWatchModules.healthcheckData import getHealthcheckData
# from nsmHealthWatchModules.healthcheckData import runHealthcheckData
from nsmHealthWatchModules.healthcheckData import fullHealthcheck
from nsmHealthWatchModules.managerData import getManagerData
from nsmHealthWatchModules.domainData import getDomainData
from nsmHealthWatchModules.comparisonData import * #TODO FIX THIS TO BE SPECIFIC
from nsmHealthWatchModules.outputData import generateFullOutput
from nsmHealthWatchModules.outputData import generateOutputsResultDictOnly
from nsmHealthWatchModules.fileGenerators import *
from nsmHealthWatchModules.policyData import getPolicies
from nsmHealthWatchModules.interfaceData import getInterfaceAssignments
from genExecutable import generateEXEandBundle

def checkExe():
    #TODO pull in extra required files (config, json files, etc.)
    from genExecutable import genExe
    generateEXEandBundle()

def dumpJson(filename, dictToDump):
    with open(filename, "w") as of:
        json.dump(dictToDump, of, indent=4)

def loadJson(filename):
    with open(filename, "r") as inf:
        jsonFile = json.load(inf)
    return jsonFile

def checkCreds():
    localFiles = os.listdir(".")

    #TODO create check if the file isn't readable as a json, then generate a new creds file and exit
    if "creds.json" not in localFiles:
        print("Generating credentials file template at 'creds.json'\nPlease add user/pass and rerun this tool")
        generateCredentialsFile()
        exit()
    else:
        requiredKeys = [
            "username",
            "password",
            "host"
        ]
        requiredKeys = sorted(requiredKeys)
        creds = loadJson("creds.json")
        if requiredKeys != sorted(list(creds.keys())):
            print("Bad creds.json file, regenerating...")
            os.remove("creds.json")
            generateCredentialsFile()
            exit()
        elif "" in creds.values() or " " in creds.values():
            print("Empty value present in creds.json")
        else:
            return creds

def getInitialData(nsmapi):
    # Done 6-1-2020
    # TODO extract ids not using the regex?

    """
    "/domain",
    "/sensors",
    # "/botnetdetectors/available/version",
    # "/signatureset/available/version",
    # "/devicesoftware/versions",
    # "/botnetdetectors/version"


    ips - /domain/{domainId}/ipspolicies
    firewall - /domain/{domainId}/firewallpolicy
    connectionlimit - /domain/{domainId}/connectionlimitingpolicies
    qos - /domain/{domainId}/qospolicy
    inspection - /protectionoptionspolicy
    malware - /domain/{domainId}/malwarepolicy
    polgroup - /domain/{domainId}/policygroups
    """
    initData = {}

    url = f"/healthcheck"
    print("Running basic healthcheck")
    healthcheckData = nsmapi.call(url, method="PUT", message='{"id":["default"]}')
    initData["healthcheck"] = healthcheckData

    for i in range(20):
        print(f".", end="", flush=True)
        time.sleep(.5)
    print("")

    print("Getting initial sensor data")
    url = "/sensors"
    basicData = json.dumps(nsmapi.call(url))
    dataType = url[1:].replace("/", "_")
    initData[dataType] = []
    for id in re.findall("\"sensorId\":.*?, \"name\":.*?,", basicData):
        if id[-1] == ",":
            id = id[:-1]
            id = id.replace("\"", "")
            id = id.replace(": ", ":")
        num, name = id.split(",")
        num = num.split(":")[-1]
        name = name.split(":")[-1]
        idName = f"{num},{name}"
        initData[dataType].append(idName)

    print("Getting initial domain data")
    url = "/domain"
    basicData = json.dumps(nsmapi.call(url))
    dataType = url[1:].replace("/", "_")
    initData[dataType] = []
    for id in re.findall("\"id\":.*?, \"name\":.*?,", basicData):
        if id[-1] == ",":
            id = id[:-1]
            id = id.replace("\"", "")
            id = id.replace(": ", ":")
        num, name = id.split(",")
        num = num.split(":")[-1]
        name = name.split(":")[-1]
        idName = f"{num},{name}"
        initData[dataType].append(idName)

    policyURLs = [
        "/domain/{domainId}/ipspolicies",
        "/domain/{domainId}/firewallpolicy",
        "/domain/{domainId}/connectionlimitingpolicies",
        "/domain/{domainId}/qospolicy",
        "/protectionoptionspolicy",
        "/domain/{domainId}/malwarepolicy",
        "/domain/{domainId}/policygroups"
    ]

    print("Getting initial policy data")
    initData["policy"] = {}
    for domain in initData["domain"]:
        domainId, domainName = domain.split(",")
        initData["policy"][domainId] = {}
        for url in policyURLs:
            url = url.replace("{domainId}", domainId)
            policyData = nsmapi.call(url)
            key = list(policyData.keys())[0]
            policyType = url.split("/")[-1].replace("policy", "").replace("policies", "")
            initData["policy"][domainId][policyType] = []
            for policy in policyData[key]:
                policy = json.dumps(policy)
                # pattern = "\"([^\"]*?)(id|ID|iD|Id){0,1}(name){0,1}\": (.*?)," - don't seem to work
                # extracted = re.findall(pattern, policy) - don'tens seem to works
                # initData["policy"][domainId][policyType]["full"] = policy
                for polK, polV in json.loads(policy).items():
                    if "omain" not in polK.lower():
                        if "name" in polK.lower():
                            name = polV
                        elif "id" in polK.lower():
                            id = polV
                initData["policy"][domainId][policyType].append((id,name))

    print("Got Initial Data")

    return initData

def updateVersionsInTemplate(results):
    # done 5-5-2020
    versionFileFileName = "currentVersions.json"
    for item in results["initData"]["healthcheck"]["summary"]:
        if item["id"] == "GetNSMVersion":
            nsmCustomerVersion = item["result"]
            nsmMajorRev = ".".join(nsmCustomerVersion.split(".")[:2])

    def generateVersionFile():
        versions = {}

        sensorModels = [
            "IPS-NS9100",
            "IPS-NS9200",
            "IPS-NS9300",
            "IPS-NS9500",
            "IPS-NS3XXX",
            "IPS-NS5XXX",
            "IPS-NS7XXX",
            "M-8000",
            "M-4050",
            "M-6050",
            "IPS-VM600",
            # "",
        ]

        majorNSMRevisions = [
            "9.1",
            "9.2",
            "10.1",
            "8.3",
            # "",
        ]

        versions["botnets"] = "bot.bot.bot.bot"
        versions["sigset"] = "sig.sig.sig.sig"
        # versions["customernsm"] = "9.1.5.33"
        # versions["customernscm"] = "9.1.5.22"
        versions["nsmVersions"] = {}
        versions["nscmVersions"] = {}
        versions["gam"] = "gam.gam.gam.gam"
        versions["sensorVersions"] = {}
        versions["sensorVersions"]["note"] = "this depends on sensor, and which  major rev of NSM...can be tricky"
        for rev in majorNSMRevisions:
            versions["sensorVersions"][rev] = {}
            versions["nsmVersions"][rev] = "man.man.man.man"
            versions["nscmVersions"][rev] = "man.man.man.man"
            for model in sensorModels:
                versions["sensorVersions"][rev][model] = "sen.sen.sen.sen"

        versions["nsmMajorRevision"] = nsmMajorRev
        versions["nsmCustomerVersion"] = nsmCustomerVersion


        with open(versionFileFileName, "w") as of:
            json.dump(versions, of, indent=8)

        return versions

    def checkForVersionFile():
        versions = {}
        if os.path.isfile(versionFileFileName):
            print(f"{versionFileFileName} is present, opening")
            try:
                with open(versionFileFileName, "r") as inf:
                    versions = json.load(inf)
            except:
                pass
        return versions

    def updateTemplate(versions):
        with open("specificOutputTemplate.json", "r") as inf:
            template = inf.read()
        template = template.replace("populateFromFile-botnets", versions["botnets"])
        template = template.replace("populateFromFile-sigset", versions["sigset"])
        template = template.replace("populateFromFile-nsm", versions["nsmVersions"][nsmMajorRev])

        with open("updatedTemplate.json", "w") as inf:
            inf.write(template)

    versions = checkForVersionFile()
    if versions == {}:
        print("versions file blank, regenerating")
        versions = generateVersionFile()

    updateTemplate(versions)
    return versions

def genReturnBundle():
    import zipfile
    import glob

    bundleFileName = "returnBundle.zip"

    filesToBundle = [
        "data.out",
        "specificOutput.json",
    ]

    globsToBundle = [
        "apiErrors.*",
        "*json",
        "*log",
        "*txt"
    ]

    for g in globsToBundle:
        for f in glob.glob(g):
            filesToBundle.append(f)

    for f in os.listdir(".temp"):
        filesToBundle.append(f".temp/{f}")

    filesToBundle = sorted(list(set(filesToBundle)))

    bundle = zipfile.ZipFile(bundleFileName, "w", compresslevel=9)

    for f in filesToBundle:
        bundle.write(f)

    bundle.close()

    pprint(zipfile.ZipFile(bundleFileName).infolist())
    print(f"{os.stat(bundleFileName).st_size / 1024 / 1024}KB")

def main():
    ONLINE = True

    try:
        os.mkdir(".temp")
    except FileExistsError:
        pass
    except:
        traceback.print_exc()

    results = {}
    results["startTime"] = time.time()
    results["startDateTime"] = datetime.datetime.utcnow().isoformat()

    print("Checking Credentials")
    try:
        creds = checkCreds()
    except:
        print("Failure when checking credentials, exiting.")
        exit()


    print("Loading Config from config.json")
    if not os.path.isfile("config.json"):
        generateConfigFile()
    with open("config.json", "r") as inf:
        results["config"] = json.load(inf)

    if results["config"]["enableDataCollection"]:

        print("Connecting to API")

        try:
            #TODO put this into the config file rather than a separate file
            nsmapi = api.apiConnector(USERNAME=creds["username"], PASSWORD=creds["password"], HOST=creds["host"], TIMEOUT=results["config"]["queryTimeout"], RETRIES=results["config"]["queryRetries"])
            if nsmapi.status()["apiconnection"] == "FAIL":
                print("API Status check failed, please check credentials/hostname. Exiting")
                exit()
        except:
            print("Could not connect to NSM API, please check credentials/hostname. Exiting")
            # traceback.print_exc()
            exit()

        # from refactorTester import getManagerData
        # getManagerData(nsmapi)


        #TODO need to check and make sure it's connected, otherwise fail

        # if ONLINE:
        #     results["config"]["enableDataCollection"] = True

        # from nsmHealthWatchModules.getAvailableVersionsFromInternet import getAvailableVersionsFromInternet
        # getAvailableVersionsFromInternet(results, nsmapi) #TODO: use this to generate the versions file

        print("Getting Initial Data")
        results["initData"] = getInitialData(nsmapi)

        print("Updating Version Template")
        results["versions"] = updateVersionsInTemplate(results) #OK 6-1-2020

        print("Getting Healthcheck Data")
        results["healthcheck"], results["healthcheckflat"] = fullHealthcheck(nsmapi)  #rewritten 9-2-2020 # OK 6-1-2020

        print("Getting Sensor Data")
        returnedSensorData = getSensorData(results, nsmapi), #THREADING WORKING 6-10-2020 #TODO:adjust threading to not have to use a global
        if type(returnedSensorData) == tuple:
            results["sensorData"] = returnedSensorData[0] #this is a shitty fix for sensorData being returned as a tuple for some reason
        #
        print("Getting Manager Data")
        results["managerData"] = getManagerData(results, nsmapi) #rewritten 9-3-2020 #OK 6-1-2020
        #
        print("Getting Domain Data")
        results["domainData"] = getDomainData(results, nsmapi) #rewritten 9-3-2020 #OK 6-1-2020
        #
        print("Getting Policy Assignments")
        results["policyAssignments"] = getPolicyAssignments(results, nsmapi) #OK 6-4-2020
        #
        print("Getting Policy Data")
        results["policies"] = getPolicies(results, nsmapi)
        #
        with open("data.out", "wb") as of:
            pickle.dump(results, of)
        #
        generateOutputsResultDictOnly(results)

        # TODO:
            # results["cloudData"] = getCloudSettings(results, nsmapi)
            #results["interfaceAssignments"] = getInterfaceAssignments(results, nsmapi)

    if results["config"]["enableAnalysis"]:

        print("Analysis Enabled")
        with open("specificOutput.json", "r") as inf:
            results = json.load(inf)

        if not ONLINE:
            updateVersionsInTemplate(results)

        with open(f"apiErrors.txt-{results['startTime']}", "r") as inf:
            results["apiErrors"] = inf.read().splitlines()

        ########### IGNORE COMP2 !!!!!!
        # from nsmHealthWatchModules.comp2 import datacomp
        # results["templateDiff"] = datacomp(results)


        results["templateDiff"] = runComparisonWithTemplates(results)

        generateFullOutput(results)
        sys.exit()
        #
        from nsmHealthWatchModules.oneOffFunctions import marineCorpsOutput, pandasStuff, policystuff
        marineCorpsOutput()
        policystuff(results=results)
        # pandasStuff(results=results)

    if "--nrb" not in sys.argv:
        print("Generating Return Bundle")
        genReturnBundle()
    print("Logging out of API")
    nsmapi.logOut()
    print("Cleaning up Temp Directory")

    if results["config"]["tempCleanup"]:
        os.rmdir(".temp")
    time.sleep(1)


if __name__ == "__main__":
    main()
    if sys.argv[0][-2:] == "py":
        if "--ge" in sys.argv:
            checkExe()
    elif sys.argv[0][-3:] == "exe":
        input("Enter to exit")
    #TODO ARGS:
    """
        - tempDirRetain
        - nousegui (once gui is implemented) 
        --ge generate executable
        --nrb don't generate return bundle
    """
