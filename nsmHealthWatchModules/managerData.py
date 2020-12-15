import os
import json
import random
import time
from pprint import pprint
import inspect
import datetime
import traceback
from nsmHealthWatchModules.getData import getData

def getManagerData(results, nsmapi):
    #DONE 5-21-20
    data = {}
    """
    "/autoupdateconfiguration/botnet"
    "/autoupdateconfiguration/sigset"
    "/customattackeditor/mcafeeformat"
    "/customattackeditor/snort"
    "/customattackeditor/attackcount"
    yields error "/domainnameexceptions/export"
    "/domainnameexceptions/ipsinspectionwhitelist"
    "/domainnameexceptions/ipsinspectionwhitelist/IPSDNEDetail/{domainName}"
    "/domainnameexceptions/ipsinspectionwhitelist/export"
    "/gticonfiguration"
    "/gticonfiguration/excludedcidr"
    "/GUIAccess/PasswordControl"
    yields error "/GUIAccess/sessioncontrol"
    yields empty list"/loginhistory"
    "/Maintenance/BackupNow"
    "/malwarearchive/list"
    "/nsm"
    "/alerts/TopN//active_botnets"
    "/alerts/TopN//attack_applications"
    "/alerts/TopN//attack_subcategories"
    "/alerts/TopN//attacker_countries"
    "/alerts/TopN//attackers"
    "/alerts/TopN//attacks"
    "/alerts/TopN//highrisk_hosts"
    "/alerts/TopN//malware_downloads"
    "/alerts/TopN//target_countries"
    "/alerts/TopN//targets"
    "/alerts/TopN//unblocked_malware_downloads"
    "/alerts/TopN//endpoint_executables"
    "users"
    404 error "/license"
    404 error "/license/obsslusage"
    """
    resources = [
    "/autoupdateconfiguration/botnet",
    "/autoupdateconfiguration/sigset",
    "/customattackeditor/mcafeeformat",
    "/customattackeditor/snort",
    "/customattackeditor/attackcount",
    # "/domainnameexceptions/ipsinspectionwhitelist", ------ TOO BIG
    "/gticonfiguration",
    "/gticonfiguration/excludedcidr",
    "/GUIAccess/PasswordControl",
    #"/GUIAccess/sessioncontrol",
    #"/loginhistory",
    "/Maintenance/BackupNow",
    "/malwarearchive/list",
    "/nsm",
    "/alerts/TopN/active_botnets",
    "/alerts/TopN/attack_applications",
    "/alerts/TopN/attack_subcategories",
    "/alerts/TopN/attacker_countries",
    "/alerts/TopN/attackers",
    "/alerts/TopN/attacks",
    "/alerts/TopN/highrisk_hosts",
    "/alerts/TopN/malware_downloads",
    "/alerts/TopN/target_countries",
    "/alerts/TopN/targets",
    "/alerts/TopN/unblocked_malware_downloads",
    "/alerts/TopN/endpoint_executables",
    "/users",
    # "/license",
    #"/license/obsslusage"
    ]

    for resource in resources:
        url = resource
        data[resource.replace("/", "_")[1:]] = getData(nsmapi, url, resource, results["startTime"])

    return data
