import time
from pprint import pprint
from nsmHealthWatchModules.getData import getData

def getPolicyAssignments(results, nsmapi):
    data = {}
    # T ODO 5-21-20
    #DONE 6-1-2020
    """
        # "/domain/{domainId}/policyassignments/interface",
        # "/domain/{domainId}/policyassignments/interface/{vidsId}",
        # "/domain/{domainId}/policyassignments/device",
        "/domain/{domainId}/policyassignments/device/{deviceid}",

    """
    resources = [
        "/domain/{domainId}/policyassignments/interface",
        "/domain/{domainId}/policyassignments/device"
    ]

    for domain in results["initData"]["domain"]:
        domainId, domainName = domain.split(",")
        for resource in resources:
            url = resource.replace("{domainId}", domainId)
            data[url.replace("/", "_")[1:]] = getData(nsmapi, url, resource, results["startTime"])

    # pprint(data)
    return data

def getPolicies(results, nsmapi):
    # TODO: v2
    # 5-21-20
    data = {}
    #TODO get actual domain IDs as passed data, it's debug data for now

    """
    "/policygroup/{policygroupid}"
    "/malwarepolicy/malwareprotocols",
    "/malwarepolicy/defaultscanningoptions",
    "/malwarepolicy/{policyId}"
    "/connectionlimitingpolicy/{policyId}"
    "/connectionlimitingpolicy/countrylist",
    "/firewallpolicy/{policyId}"
    "/ipspolicy/{policyId}"
    "/protectionoptionspolicy",
    "/protectionoptionspolicy/{policyid}"
    "/qospolicy/{policyId}"
    # "/domain/{domainId}/connectionlimitingpolicies",
    # "/domain/{domainId}/defaultipspolicies",
    # "/domain/{domainId}/defaultreconpolicies",
    # "/domain/{domainId}/malwarepolicy/export",
    # "/domain/{domainId}/firewallpolicy/export",
    # "/domain/{domainId}/policygroups",
    """



    domainPolicyURIs = [
    "/domain/{domainId}/qospolicy",
    "/domain/{domainId}/connectionlimitingpolicies",
    "/domain/{domainId}/defaultipspolicies",
    "/domain/{domainId}/defaultreconpolicies",
    "/domain/{domainId}/malwarepolicy/export",
    "/domain/{domainId}/firewallpolicy/export",
    "/domain/{domainId}/policygroups",
    "/protectionoptionspolicy"
    ]

    basePolicyDataByDomain = {}
    initialPolicyIDMapping = {}
    finalPolicyIDMapping = {}
    uniquePolicies = {}
    policyDetails = {}

    for domain in results["initData"]["domain"]:
        basePolicyDataByDomain[domain] = {}
        initialPolicyIDMapping[domain] = {}
        domainID, domainName = domain.split(",")
        # protectionOptionsPolicy = getData(nsmapi, "/protectionoptionspolicy", "protectionoptionspolicy", results["startTime"])
        # basePolicyDataByDomain[domain]["protectionoptionspolicy"] = protectionOptionsPolicy
        # policyIDMapping[domain]["protectionoptionspolicy"] = {}
        for uri in domainPolicyURIs:
            if "protectionoptionspolicy" in uri:
                resource = "protectionoptionspolicy"
            else:
                resource = "_".join(uri.split("/")[3:4])
            uri = uri.replace("{domainId}", domainID)
            # print(uri, resource)
            returnedData = getData(nsmapi, uri, resource, results["startTime"])
            for policyName, policies in returnedData.items():
                basePolicyDataByDomain[domain][resource] = policies
                initialPolicyIDMapping[domain][resource] = {}
                for policy in policies:
                    if "policyName" in policy.keys():
                        initialPolicyIDMapping[domain][resource][policy["policyId"]] = policy["policyName"]
                    elif "name" in policy.keys():
                        initialPolicyIDMapping[domain][resource][policy["policyGroupId"]] = policy["name"]

    # pprint(basePolicyDataByDomain)
    # pprint(initialPolicyIDMapping)


    import traceback
    for domain, policies in initialPolicyIDMapping.items():
        for policyType, pols in policies.items():
            finalPolicyIDMapping[policyType] = {}
            uniquePolicies[policyType] = {}
            for policyId, policyName in pols.items():
                finalPolicyIDMapping[policyType][policyId] = policyName
                if "default" not in policyName.lower():
                    uniquePolicies[policyType][policyId] = policyName

    # pprint(finalPolicyIDMapping)
    #TODO How to deal with the master attack repo???????????? 7-16-20@2359
    # pprint(uniquePolicies)

    specificPolicyURIs = [
        "/policygroup/{policyId}", ##### should be "/policygroup/{policygroupid}", but it's changed to policyId to ease the find and replace
        "/malwarepolicy/{policyId}",
        "/connectionlimitingpolicy/{policyId}",
        "/firewallpolicy/{policyId}",
        "/ipspolicy/{policyId}",
        "/protectionoptionspolicy/{policyId}",
        "/qospolicy/{policyId}"
    ]

    for uri in specificPolicyURIs:
        resource = uri.split("/")[1]
        policyDetails[resource] = {}
        if resource == "ipspolicy":
            pass
            ###TODO: what's pulled from the API here isn't helpful and it's huge, so it's being omitted for now
            ###TODO: update 8/1/20 - new work to be done with Lucas

            # for pid, name in uniquePolicies["defaultipspolicies"].items():
            #     print(pid, resource, name)
            #     policyDetails[resource][pid] = getData(nsmapi, uri.replace("{policyId}", str(pid)), resource, results["startTime"])
        elif resource == "policygroup":
            for pid, name in uniquePolicies["policygroups"].items():
                # print(pid, resource, name)
                policyDetails[resource][pid] = getData(nsmapi, uri.replace("{policyId}", str(pid)), resource, results["startTime"])
        elif resource == "malwarepolicy":
            for pid, name in uniquePolicies["malwarepolicy"].items():
                # print(pid, resource, name)
                policyDetails[resource][pid] = getData(nsmapi, uri.replace("{policyId}", str(pid)), resource, results["startTime"])
        elif resource == "connectionlimitingpolicy":
            for pid, name in uniquePolicies["connectionlimitingpolicies"].items():
                # print(pid, resource, name)
                policyDetails[resource][pid] = getData(nsmapi, uri.replace("{policyId}", str(pid)), resource, results["startTime"])
        elif resource == "firewallpolicy":
            for pid, name in uniquePolicies["firewallpolicy"].items():
                # print(pid, resource, name)
                policyDetails[resource][pid] = getData(nsmapi, uri.replace("{policyId}", str(pid)), resource, results["startTime"])
        elif resource == "protectionoptionspolicy":
            for pid, name in uniquePolicies["protectionoptionspolicy"].items():
                # print(pid, resource, name)
                policyDetails[resource][pid] = getData(nsmapi, uri.replace("{policyId}", str(pid)), resource, results["startTime"])
        elif resource == "qospolicy":
            for pid, name in uniquePolicies["qospolicy"].items():
                # print(pid, resource, name)
                policyDetails[resource][pid] = getData(nsmapi, uri.replace("{policyId}", str(pid)), resource, results["startTime"])

    policyData = {}
    policyData["basePolicyDataByDomain"] = basePolicyDataByDomain
    policyData["policyIDMapping"] = finalPolicyIDMapping
    policyData["uniquePolicyIDs"] = uniquePolicies
    policyData["policyDetails"] = policyDetails

    return policyData

    """
    
    # exit(0)
    #
    #
    # resources = {}
    # resources["malwarepolicy"] = {}
    # resources["malwarepolicy"]["idURL"] = ["/domain/{domainId}/malwarepolicy"]
    # resources["malwarepolicy"]["IDs"] = []
    # resources["connectionlimitingpolicy"] = {}
    # resources["connectionlimitingpolicy"]["idURL"] = []
    # resources["connectionlimitingpolicy"]["IDs"] = []
    # resources["firewallpolicy"] = {}
    # resources["firewallpolicy"]["idURL"] = ["/domain/{domainId}/firewallpolicy"]
    # resources["firewallpolicy"]["IDs"] = []
    # resources["ipspolicy"] = {}
    # resources["ipspolicy"]["idURL"] = ["/domain/{domainId}/ipspolicies"]
    # resources["ipspolicy"]["IDs"] = []
    # resources["policygroup"] = {}
    # resources["policygroup"]["idURL"] = []
    # resources["policygroup"]["IDs"] = []
    # resources["protectionpolicy"] = {}
    # resources["protectionpolicy"]["idURL"] = []
    # resources["protectionpolicy"]["IDs"] = []
    # resources["qospolicy"] = {}
    # resources["qospolicy"]["idURL"] = ["/domain/{domainId}/qospolicy"]
    # resources["qospolicy"]["IDs"] = []
    # resources["ratelimitingpolicy"] = {}
    # resources["ratelimitingpolicy"]["idURL"] = ["/domain/{domainId}/ratelimitingprofiles"]
    # resources["ratelimitingpolicy"]["IDs"] = []
    # # resources[""] = {}
    # # resources[""]["idURL"] = []
    # # resources[""]["IDs"] = []
    #
    # resources["malware"]["urls"] = [
    #     "/malwarepolicy/malwareprotocols",
    #     "/malwarepolicy/defaultscanningoptions",
    #     "/malwarepolicy/{policyId}"
    # ]
    #
    # resources["connectionlimiting"]["urls"] = [
    #     "/connectionlimitingpolicy/countrylist",
    #     "/connectionlimitingpolicy/{policyId}"
    # ]
    #
    # resources["firewall"]["urls"] = [
    #     "/firewallpolicy/{policyId}"
    # ]
    #
    # resources["ipspolicy"]["urls"] = [
    #     "/ipspolicy/{policyId}"
    # ]
    #
    # resources["policygroup"]["urls"] = [
    #     "/policygroup/{policygroupid}"
    # ]
    #
    # resources["protectionpolicy"]["urls"] = [
    #     "/protectionoptionspolicy",
    #     "/protectionoptionspolicy/{policyid}"
    # ]
    # resources["qospolicy"]["urls"] = [
    #     "/qospolicy/{policyId}"
    # ]

    # ####Get policy IDs####
    #
    # domainPolicyResourceURLs = []
    #
    # for policyResource in policyIDResourceURLs:
    #     for id in domainIDs:
    #         domainPolicyResourceURLs.append(policyResource.replace("{domainId}", id))
    # # pprint(domainPolicyResourceURLs)
    # basicPolicyInfo = {}
    # for url in domainPolicyResourceURLs:
    #     polType = url.split("/")[-1]
    #     print(url)
    #     basicPolicyInfo[polType] = getData(nsmapi, url, url, results["startTime"])


    # for resource in resources:
    #     if "{policy" in resource:
    #         print(resource)


    # for resource in resources:
    #     url = resource
    #     data[resource.replace("/", "_")[1:]] = getData(nsmapi, url, resource, results["startTime"])
    #
    # return data
"""