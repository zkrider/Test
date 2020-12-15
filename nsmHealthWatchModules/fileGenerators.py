import os
import json
import random
import time
from pprint import pprint
import inspect
import datetime
import traceback

def writeGeneratedFile(fileName, fileData):
    with open(fileName, "w") as of:
        json.dump(fileData, of, indent=8)


def generateConfigFile():
    params = {}
    params["credsFile"] = "creds.json"
    params["numSensorsToQuerySimultaneously"] = 3
    params["DEBUG"] = False
    params["queryTimeout"] = 60
    params["queryRetries"] = 10
    params["enableAnalysis"] = True
    params["enableDataCollection"] = True
    # params[""] = ""

    params["externalIntegrations"] = {}
    params["externalIntegrations"]["atd"] = 0
    params["externalIntegrations"]["gam"] = 0
    params["externalIntegrations"]["epo"] = 0
    params["externalIntegrations"]["gti"] = 0
    params["externalIntegrations"]["ntba"] = 0
    params["externalIntegrations"]["tie/dxl"] = 0
    params["externalIntegrations"]["inboundssl"] = 0
    params["externalIntegrations"]["outboundssl"] = 0
    # params["externalIntegrations"][""] = 0

    params["enableAnalysis"] = True
    params["enableDataCollection"] = True

    writeGeneratedFile("config.json", params)

def generateFindingsTemplateFile():
    pass

def generateCredentialsFile():
    creds = {}
    creds["username"] = ""
    creds["password"] = ""
    creds["host"] = ""

    writeGeneratedFile("creds.json", creds)

def generateVersionsFile():
    pass

"""def generate():
    pass

def generate():
    pass

def generate():
    pass

def generate():
    pass

def generate():
    pass"""