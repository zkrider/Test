import os
import json
import random
import time
from pprint import pprint
import inspect
import datetime
import traceback
from nsmHealthWatchModules.getData import getData


def getAvailableVersionsFromInternet(results, nsmapi):
    #TODO Needs some tweaks, specifically to pick out the latest version for each major rev

    data = {}
    data["startTime"] = results["startTime"]
    data["startDateTime"] = results["startDateTime"]

    uris = [
    "/botnetdetectors/available/version",
    "/signatureset/available/version",
    "/devicesoftware/versions"
    ]


    for uri in uris:
        resource = "".join(uri[1:]).replace("/", "_")
        print(resource)
        data[resource] = getData(nsmapi, uri, resource, results["startTime"])

    with open("availVersions.json", "w") as of:
        json.dump(data, of, indent=8)

