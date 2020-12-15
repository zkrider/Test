import os
import json
import random
import time
from pprint import pprint
import inspect
import datetime
import traceback
from nsmHealthWatchModules.getData import getData


def getDomainData(results, nsmapi):
    # TODO 5-21-20
    """
    "/monitors",
    "/monitors/domain/{domainId}/attacksovertime",
    "/monitors/domain/{domainId}/highcpuusage",
    "/monitors/domain/{domainId}/highflowusage",
    "/monitors/domain/{domainId}/highthroughputusage"
    "/domainnameexceptions",
    "/ratelimitingprofile/{profileId}"
    "/domain/{domainId}",
    "/domain/{domainId}/attackfilter82",
    "/domain/{domainId}/attackfilter82/{ruleId}",
    "/domain/{domainId}/attackfilter/{attackId}",
    "/domain/{domainId}/quarantineZone/{quarantineZoneID}",
    "/domain/{domainId}/quarantineZone",
    "/domain/{domainId}/ruleobject",
    "/domain/{domainId}/connectionlimitingpolicies",
    "/domain/{domainId}/nonstandardports",
    "/domain/{domainId}/filereputation/gti",
    "/domain/{domainId}/filereputation/gti/filetypes",
    "/domain/{domainId}/filereputation/fingerprintscount",
    "/domain/{domainId}/filereputation/filetypes",
    "/domain/{domainId}/passivedeviceprofiling",
    "/domain/{domainId}/virtualization/setting",
    "/domain/{domainId}/device",
    "/domain/{domainId}/device/{deviceId}",
    "/domain/{domainId}/eia",
    "/domaingetdomain/{domainId}",
    "/domain{domainId}/defaultipspolicies",
    "/domain{domainId}/defaultreconpolicies",
    "/domain/{domainId}/notification/faults/syslog",
    "/domain/{domainId}/notification/firewall/syslog",
    "/domain/{domainId}/nameresolution",
    "/domain/{domainId}/ipsreconpolicy/export",
    "/domain/{domainId}/remoteaccess/tacacs",
    "/domain/{domainId}/nmsusers",
    "/domain/{domainId}/nmsuser/{userId}",
    "/domain/{domainId}/failoverpair",
    "/domain/{domainId}/failoverpair/{clusterId}",
    "/domain/{domainId}/nmsips",
    #"/domain/{domainId}/malwarepolicy/export",
    #"/domain/{domainId}/firewallpolicy/export",
    "/domain/{domainId}/exceptions/export",
    "/domain/{domainId}/directsyslog",
    "/domain/{domainId}/activebotnets",
    "/domain/{domainId}/activebotnetzombies/{botId}",
    "/domain/{domainId}/ipsdevices/atdintegration",
    "/domain/{domainId}/ipsdevices/quarantine",
    "/domain/{domainId}/networkforensicsintegration",
    "/domain/{domainId}/packetcaptureruletemplate",
    "/domain/{domainId}/packetcaptureruletemplate/{name}",
    #"/domain/{domainId}/policygroups",
    "/domain/{domainId}/epointegration",
    "/domain/{domainId}/dxlintegration",
    "/domain/{domainId}/remoteaccess/radius",
    "/domain/{domainId}/collectionsettings",
    "/domain/{domainId}/collectionsettings",
    "/domain/{domainId}/cadsintegration",
    "/domain/{domainId}/cadsintegration/testmanagerconnection",
    "/domain/{domainId}/cadsintegration/testsensorconnection",
    "/domain/{domainId}/advanceddeviceconfiguration",
    "/domain/proxyserver",
    "/domain{domainId}/proxyserver",
    "/domain/{domainId}/sslconfiguration",
    "/domain/sslconfiguration/resigncert",
    "/domain/sslconfiguration/generateresigncert",
    "/domain/sslconfiguration/exportresigncert",
    "/domain/sslconfiguration/trustedcerts",
    "/domain/sslconfiguration/trustedcert",
    "/domain/sslconfiguration/updatedefaulttrustedcerts",
    "/domain/sslconfiguration/internalwebservercerts",
    "/domain/{domainId}/outboundsslexceptions",
    "/domain/{domainId}/outboundsslexceptions/{ruleId}",
    "/domain/{domainId}/performancemonitoring",
    #"/domain{domainId}/attacksetprofile/rulesetdetails/{policyId}",
    "/domain{domainId}/attacksetprofile/getallrules"
    "/domain/{domainId}/malwaredownloads"

    "/domain/{domainId}/threatexplorer/alerts/TopN/{count}/direction/{direction}/duration/{duration}",
    "/domain/{domainId}/threatexplorer/alerts/TopN/{count}/direction/{direction}/duration/{duration}/attacks",
    "/domain/{domainId}/threatexplorer/alerts/TopN/{count}/direction/{direction}/duration/{duration}/attackers",
    "/domain/{domainId}/threatexplorer/alerts/TopN/{count}/direction/{direction}/duration/{duration}/targets",
    "/domain/{domainId}/threatexplorer/alerts/TopN/{count}/direction/{direction}/duration/{duration}/attack_applications",
    "/domain/{domainId}/threatexplorer/alerts/TopN/{count}/direction/{direction}/duration/{duration}/malware",
    "/domain/{domainId}/threatexplorer/alerts/TopN/{count}/direction/{direction}/duration/{duration}/executables"
    """




    resources = [
    ##### "/ratelimitingprofile/{profileId}",  - NEED TO MOVE TO ANOTHER SECTION???
    "/monitors/domain/{domainId}/attacksovertime",
    "/monitors/domain/{domainId}/highcpuusage",
    "/monitors/domain/{domainId}/highflowusage",
    "/monitors/domain/{domainId}/highthroughputusage",
    "/domainnameexceptions",
    ## "/domain/{domainId}/attackfilter82",
    ## "/domain/{domainId}/attackfilter82/{ruleId}",
    ## "/domain/{domainId}/attackfilter/{attackId}",
    ## "/domain/{domainId}/quarantineZone/{quarantineZoneID}",
    "/domain/{domainId}/quarantineZone",
    # "/domain/{domainId}/ruleobject",   #### - Getting an error back?
    "/domain/{domainId}/nonstandardports",
    "/domain/{domainId}/filereputation/gti",
    "/domain/{domainId}/filereputation/gti/filetypes",
    "/domain/{domainId}/filereputation/fingerprintscount",
    "/domain/{domainId}/filereputation/filetypes",
    "/domain/{domainId}/passivedeviceprofiling",
    "/domain/{domainId}/virtualization/setting",
    "/domain/{domainId}/device",
    ##"/domain/{domainId}/eia", ### not documentated in the API guide?
    "/domain/{domainId}/notification/faults/syslog",
    "/domain/{domainId}/notification/firewall/syslog",
    "/domain/{domainId}/nameresolution",
    "/domain/{domainId}/remoteaccess/tacacs",
    "/domain/{domainId}/nmsusers",
    "/domain/{domainId}/nmsips",
    "/domain/{domainId}/failoverpair",
    "/domain/{domainId}/exceptions/export",
    "/domain/{domainId}/directsyslog",
    "/domain/{domainId}/activebotnets",
    "/domain/{domainId}/ipsdevices/atdintegration",
    "/domain/{domainId}/ipsdevices/quarantine",
    # "/domain/{domainId}/networkforensicsintegration", ####-----ERROR
    "/domain/{domainId}/epointegration",
    "/domain/{domainId}/dxlintegration",
    "/domain/{domainId}/remoteaccess/radius",
    "/domain/{domainId}/collectionsettings",
    "/domain/{domainId}/cadsintegration",
    # "/domain/{domainId}/cadsintegration/testmanagerconnection",
    # "/domain/{domainId}/cadsintegration/testsensorconnection",
    "/domain/{domainId}/advanceddeviceconfiguration",
    # "/domain/proxyserver",  #_------- how is this different than the one below??
    "/domain/{domainId}/proxyserver",
    "/domain/{domainId}/sslconfiguration",
    "/domain/{domainId}/outboundsslexceptions",
    "/domain/{domainId}/performancemonitoring",
    "/domain/{domainId}/attacksetprofile/getallrules",
    "/domain/{domainId}/malwaredownloads"

    # "/domain/{domainId}/threatexplorer/alerts/TopN/{count}/direction/{direction}/duration/{duration}",
    # "/domain/{domainId}/threatexplorer/alerts/TopN/{count}/direction/{direction}/duration/{duration}/attacks",
    # "/domain/{domainId}/threatexplorer/alerts/TopN/{count}/direction/{direction}/duration/{duration}/attackers",
    # "/domain/{domainId}/threatexplorer/alerts/TopN/{count}/direction/{direction}/duration/{duration}/targets",
    # "/domain/{domainId}/threatexplorer/alerts/TopN/{count}/direction/{direction}/duration/{duration}/attack_applications",
    # "/domain/{domainId}/threatexplorer/alerts/TopN/{count}/direction/{direction}/duration/{duration}/malware",
    # "/domain/{domainId}/threatexplorer/alerts/TopN/{count}/direction/{direction}/duration/{duration}/executables"

    ]

    domainData = {}
    for domainIDName in sorted(results["initData"]["domain"]):
        domainData[domainIDName] = {}
        domainId = domainIDName.split(",")[0]
        for resource in resources:
            url = resource
            url = url.replace("{domainId}", domainId)
            url = url.replace("{domainId}", domainId)
            url = url.replace("{domainID}", domainId)

            ####COMMENT yes, there should be 3 of these to account for differences in caps in the api
            # print("res", resource)
            # print("url", url)
            resourceKey = resource.split("{dom")[-1].split("/", 1)[-1].replace("/", "_")
            domainData[domainIDName][resourceKey] = getData(nsmapi, url, resource, results["startTime"])

    return domainData
    """
    maybe don't need
                            # def getData(url, sensorId, resource):
                        #     print(url, resource)
                        #     while True:
                        #         reply = nsmapi.call(url)
                        #         if type(reply) != dict:
                        #             print("Reply is not a dict...that's an error")
                        #             print("Reply:")
                        #             print(reply)
                        #             break
                        #         try:
                        #             keys = reply.keys()
                        #             if "errorMessage" in keys or "errorId" in keys:
                        #                 output = f"{url}, {sensorId}, {resource}, {reply}"
                        #                 with open(f"apiErrors.txt-{startTime}", "a") as of:
                        #                     of.write(output)
                        #                     of.write("\n")
                        #                 # print("-----------")
                        #                 # print("error")
                        #                 # print(output)
                        #                 # print("-----------")
                        #             break
                        #         except:
                        #             print("couldn't find any keys")
                        #             print(reply)
                        #     return reply

    """
