import os
import json
import random
import time
from pprint import pprint
import inspect
import datetime
import traceback
from nsmHealthWatchModules.getData import getData

def getInterfaceAssignments(results, nsmapi):
    # TODO 5-21-20
    """
    "/sensor/{sensorId}/interface/{interfaceId}",
    "/sensor/{sensorId}/interface/{interfaceId}/attackfilter/{attackId}",
    "/sensor/{sensorId}/interface/{interfaceId}/allocatedcidrlist",
    "/sensor/{sensorId}/interface/{interfaceId}/virtualization/setting",
    "/sensor/{sensorId}/interface/{interfaceId}/localipspolicy"
    "/sensor/{sensorId}/port/{portId}/ipsdevices/quarantine",
    ERROR                        "/sensor/{sensorId}/port/{portId}/ipsettings",
    ERROR                        "/sensor/{sensorId}/port/{portId}/trafficstats/droppedpackets",
    ERROR                        "/sensor/{sensorId}/port/{portId}/trafficstats/trafficrxtx"
    NEED TO USE VS SENSOR/STATUS                        "/sensor/{sensorId}/port/{portId}",
    """
    resources = [
    # "/sensor/{sensorId}/port/{portId}/ipsdevices/quarantine",
    # "/sensor/{sensorId}/port/{portId}/ipsettings",
    # "/sensor/{sensorId}/port/{portId}/trafficstats/droppedpackets", - Doesn't work with virtual
    # "/sensor/{sensorId}/port/{portId}/trafficstats/trafficrxtx", - Doesn't work with virtual
    # "/sensor/{sensorId}/port/{portId}"
    "/sensor/{sensorId}/port/{portId}/trafficstats/droppedpackets",
    "/sensor/{sensorId}/port/{portId}/trafficstats/trafficrxtx"
    ]

    # TODO: Need To Get Domains and Policies before running this
    #TODO STOPPED HERE!!!!! 6-1-2020

    for resource in resources:
        for sensor, data in results["sensorData"].items():
            print(sensor)
            url = resource.replace("{sensorId}", sensor.split(",")[0])
            for intf in data["Ports"]:
                    # print(intf)
                    url = url.replace("{portId}", str(intf["portId"]))
                    print(url)
                    reply = nsmapi.call(url)
                    pprint(reply)


    # for sensor, data in interfaces:
    #     print(sensor)
    #     for intf in sensor:
    #         print(intf)
    #
    return ""
    # return interfaces
    for domainIDName in sorted(results["initData"]["domain"]):
        domainData[domainIDName] = {}
        domainId = domainIDName.split(",")[0]
        print(domainId)
        for resource in resources:
            url = resource
            url = url.replace("{domainId}", domainId)
            url = url.replace("{domainID}", domainId)
            ####COMMENT yes, there should be 3 of these to account for differences in caps in the api
            # print("res", resource)
            # print("url", url)
            resourceKey = resource.split("{dom")[-1].split("/", 1)[-1].replace("/", "_")
            domainData[domainIDName][resourceKey] = getData(nsmapi, url, resource, startTime)

