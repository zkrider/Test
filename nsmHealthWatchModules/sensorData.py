import os
import json
import random
import time
from pprint import pprint
import inspect
import datetime
import traceback
from nsmHealthWatchModules.getData import getData
import threading
import string

sensorData = {}

def sensorCLICommands():
    #TODO: v2
    pass

def sensorDataWorker(sensor, nsmapi, startTime):
    global sensorData
    def get_sensor_data(url, sensorId, resource):
        print(url, resource)
        while True:
            reply = nsmapi.call(url)
            if type(reply) != dict:
                print("Reply is not a dict...that's an error")
                print("Reply:")
                print(reply)
                break
            try:
                keys = reply.keys()
                if "errorMessage" in keys or "errorId" in keys:
                    output = f"{url}, {sensorId}, {resource}, {reply}"
                    with open(f"apiErrors.txt-{startTime}", "a") as of:
                        of.write(output)
                        of.write("\n")
                    # print("-----------")
                    # print("error")
                    # print(output)
                    # print("-----------")
                break
            except:
                print("couldn't find any keys")
                print(reply)

        return reply


    st = time.time()
    # print(sensor)
    sensorId = sensor.split(",")[0]

    sensorData[sensor]["top10"] = {}

    url = f"/sensor/{sensorId}"
    detailedSensorData = nsmapi.call(url)
    sensorData[sensor]["Interfaces"] = detailedSensorData["SensorInfo"]["Interfaces"]["InterfaceInfo"]
    sensorData[sensor]["Ports"] = detailedSensorData["SensorInfo"]["Ports"]["PortInfo"]

    resource = "sensorUpdateInfo"
    url = f"/sensor/{sensorId}/action/update_sensor_config"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)

    # resource = ""
    # url = "/sensor/{sensorId}/config/status"
    # sensorData[sensor][resource] = getData(url, sensorId, resource)

    # resource = ""
    # url = "/sensor/{sensorId}/status"
    # sensorData[sensor][resource] = getData(url, sensorId, resource)

    resource = "statelessScanningExceptionEnabled"
    url = f"/sensor/{sensorId}/scanningexception/status"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)

    resource = "statelessScanningException"
    url = f"/sensor/{sensorId}/scanningexception"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)

    resource = "ipv6"
    url = f"/sensor/{sensorId}/ipv6"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)

    resource = "quarantinedhost"
    url = f"/sensor/{sensorId}/action/quarantinehost"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)

    resource = "quarantinedhostdetails"
    url = f"/sensor/{sensorId}/action/quarantinehost/details"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)

    resource = "performancestats"
    url = f"/sensor/{sensorId}/performancestats"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)
    sensorData[sensor]["top10"][resource] = get_sensor_data(url, sensorId, resource)

    resource = "performancemonitoring"
    url = f"/sensor/{sensorId}/performancemonitoring"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)
    sensorData[sensor]["top10"][resource] = get_sensor_data(url, sensorId, resource)

    resource = "nonstandardports"
    url = f"/sensor/{sensorId}/nonstandardports"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)

    # resource = "sslkey" #This is apparently broken ---update 9-17-2020 may not work on 9.2 appliances? may be good for =< 10.1?
    # url = f"/sensor/{sensorId}/action/sslkey"
    # sensorData[sensor][resource] = getData(url, sensorId, resource)

    resource = "simulatedblockingStatus"
    url = f"/sensor/{sensorId}/simulatedblocking"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)
    sensorData[sensor]["top10"][resource] = get_sensor_data(url, sensorId, resource)

    resource = "layer7datacollectionStatus"
    url = f"/sensor/{sensorId}/layer7datacollection"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)
    sensorData[sensor]["top10"][resource] = get_sensor_data(url, sensorId, resource)

    resource = "passivedeviceprofiling"
    url = f"/sensor/{sensorId}/passivedeviceprofiling"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)
    sensorData[sensor]["top10"][resource] = get_sensor_data(url, sensorId, resource)

    resource = "attackcompilation"
    url = f"/sensor/{sensorId}/attackcompilation"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)

    # resource = "sslconfiguration" #This is apparently broken?!
    # url = f"/sensor/{sensorId}/sslconfiguration"
    # sensorData[sensor][resource] = getData(url, sensorId, resource)

    resource = "ipsettings"
    url = f"/sensor/{sensorId}/ipsettings"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)

    resource = "tcpsettings"
    url = f"/sensor/{sensorId}/tcpsettings"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)

    resource = "nmsusers"
    url = f"/sensor/{sensorId}/nmsusers"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)

    # resource = ""
    # url = "/sensor/{sensorId}/nmsusers/available"
    # sensorData[sensor][resource] = getData(url, sensorId, resource)

    #
    # resource = ""
    # url = "/sensor/{sensorId}/nmsuser/{userId}"
    # sensorData[sensor][resource] = getData(url, sensorId, resource)

    resource = "alertsupression"
    url = f"/sensor/{sensorId}/ipsalerting/alertsuppression"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)

    resource = "nmsips"
    url = f"/sensor/{sensorId}/nmsips"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)

    # resource = ""
    # url = "/sensor/{sensorId}/nmsips/available"
    # sensorData[sensor][resource] = getData(url, sensorId, resource)

    resource = "firewalllogging"
    url = f"/sensor/{sensorId}/firewalllogging"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)

    resource = "directsyslog"
    url = f"/sensor/{sensorId}/directsyslog"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)

    resource = "applicationidentification"
    url = f"/sensor/{sensorId}/policy/applicationidentification"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)
    sensorData[sensor]["top10"][resource] = get_sensor_data(url, sensorId, resource)

    resource = "ntbaintegration"
    url = f"/sensor/{sensorId}/ntbaintegration"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)

    resource = "atdintegration"
    url = f"/sensor/{sensorId}/atdintegration"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)

    # resource = ""
    # url = "/sensor/{sensorId}/importconfiguration/{requestId}"
    # sensorData[sensor][resource] = getData(url, sensorId, resource)

    resource = "dosprofilesonmanager"
    url = f"/sensor/{sensorId}/dosprofilesonmanager"
    # print(url, resource)
    sensorData[sensor][resource] = nsmapi.call(url)

    resource = "dospacketforwarding"
    url = f"/sensor/{sensorId}/dospacketforwarding"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)

    resource = "packetcapture"
    url = f"/sensor/{sensorId}/packetcapture"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)

    # resource = ""
    # url = "/sensor/{sensorId}/packetcaptureruletemplate"
    # sensorData[sensor][resource] = getData(url, sensorId, resource)

    resource = "packetcapturepcapfiles"
    url = f"/sensor/{sensorId}/packetcapturepcapfiles"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)

    # resource = ""
    # url = "/sensor/{sensorId}/packetcapturepcapfile"
    # sensorData[sensor][resource] = getData(url, sensorId, resource)

    resource = "dxlintegration"
    url = f"/sensor/{sensorId}/dxlintegration"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)

    resource = "gamupdatesettings"
    url = f"/sensor/{sensorId}/gamupdatesettings"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)

    # resource = ""
    # url = "/sensor/{sensorId}/deploydevicesoftware/{swVersion}"
    # sensorData[sensor][resource] = getData(url, sensorId, resource)

    # resource = ""
    # url = "/sensor/{sensorId}/deploydevicesoftware/{requestId}"
    # sensorData[sensor][resource] = getData(url, sensorId, resource)

    resource = "deployddevicesoftware"
    url = f"/sensor/{sensorId}/deploydevicesoftware/"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)

    # resource = ""
    # url = "/sensor/{sensorId}/diagnosticstrace/upload"
    # print(url, resource)
    # sensorData[sensor][resource] = nsmapi.call(url)

    resource = "diagnosticstrace"
    url = f"/sensor/{sensorId}/diagnosticstrace"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)

    resource = "tacacs"
    url = f"/sensor/{sensorId}/remoteaccess/tacacs"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)

    resource = "cadsintegration"
    url = f"/sensor/{sensorId}/cadsintegration"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)

    # resource = ""
    # url = "/sensor/{sensorId}/cadsintegration/testmanagerconnection"
    # sensorData[sensor][resource] = getData(url, sensorId, resource)

    #
    # resource = ""
    # url = "/sensor/{sensorId}/cadsintegration/testsensorconnection"
    # sensorData[sensor][resource] = getData(url, sensorId, resource)

    resource = "advanceddeviceconfiguration"
    url = f"/sensor/{sensorId}/advanceddeviceconfiguration"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)
    sensorData[sensor]["top10"][resource] = get_sensor_data(url, sensorId, resource)

    resource = "flows"
    url = f"/sensor/{sensorId}/trafficstats/flows"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)

    resource = "malwarestatsgroupbyengine"
    url = f"/sensor/{sensorId}/trafficstats/malwarestatsgroupbyengine"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)
    sensorData[sensor]["top10"][resource] = get_sensor_data(url, sensorId, resource)

    resource = "malwarestatsgroupbyfile"
    url = f"/sensor/{sensorId}/trafficstats/malwarestatsgroupbyfile"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)
    sensorData[sensor]["top10"][resource] = get_sensor_data(url, sensorId, resource)

    resource = "advcallbackdetectionstats"
    url = f"/sensor/{sensorId}/trafficstats/advcallbackdetectionstats"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)
    sensorData[sensor]["top10"][resource] = get_sensor_data(url, sensorId, resource)

    resource = "outboundsslstats"
    url = f"/sensor/{sensorId}/trafficstats/outboundsslstats"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)

    resource = "sensorsslstats"
    url = f"/sensor/{sensorId}/trafficstats/sensorsslstats"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)

    resource = "sslinternalwebcertmatches"
    url = f"/sensor/{sensorId}/trafficstats/sslinternalwebcertmatches"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)

    # resource = ""
    # url = "/sensor/{sensorId}/trafficstats/resetsslcounters"
    # sensorData[sensor][resource] = getData(url, sensorId, resource)

    resource = "decryptionsettings"
    url = f"/sensor/{sensorId}/decryptionsettings"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)

    ### DEVICES SECTION
    resource = "nameresolution"
    url = f"/device/{sensorId}/{resource}"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)

    resource = "proxyserver"
    url = f"/device/{sensorId}/{resource}"
    sensorData[sensor][resource] = get_sensor_data(url, sensorId, resource)

    # if sensorData[sensor]["isNTBA"]:
    #     resource = "collectionsettings"
    #     url = f"/device/{sensorId}/{resource}"
    #     print(url, resource)
    #     sensorData[sensor][resource] = nsmapi.call(url)


    print(time.time() - st)

    # sensorData.1007,tomssensor1.top.performancemonitoring.inheritSettings
    # sensorData.1007,tomssensor1.top.performancemonitoring.enableMetricCollection
    # sensorData.1007,tomssensor1.top.performancemonitoring.enableCPUUtilizationMetricCollection
    # sensorData.1007,tomssensor1.top.performancemonitoring.enablePortThroughputUtilizationMetricCollection
    # sensorData.1007,tomssensor1.top.simulatedblockingStatus.SimulatedBlockingOptionForSensor
    # sensorData.1007,tomssensor1.top.layer7datacollectionStatus.flows
    # sensorData.1007,tomssensor1.top.layer7datacollectionStatus.protocols
    # sensorData.1007,tomssensor1.top.applicationidentification.enableApplicationIdentification
    # sensorData.1007,tomssensor1.top.advanceddeviceconfiguration.preAttackBytestoCapture
    # sensorData.1007,tomssensor1.top.advanceddeviceconfiguration.inspectTunneledTraffic
    # sensorData.1007,tomssensor1.top.advanceddeviceconfiguration.inheritSettings
    # sensorData.1007,tomssensor1.top.advanceddeviceconfiguration.useTraditionalSnort
    # sensorData.1007,tomssensor1.sensorUpdateInfo.lastUpdateTime - calc it was pushed in the last week
    # sensorData.1007,tomssensor1.ipv6.ipv6Mode


def testWorker(sensor):
    print(sensor, "STARTING THREAD")
    sleepyTime = random.randint(5, 10)
    name = ''.join(random.choices(string.ascii_uppercase +
                           string.digits, k=10))
    time.sleep(sleepyTime)
    return name, f"HI THERE, I WAITING FOR {sleepyTime} seconds!"

def getSensorData(results, nsmapi):
    global sensorData
    NUMWORKERS = results["config"]["numSensorsToQuerySimultaneously"]
    #ADDED MT 6-4-2020
    #TODO NEED TO TWEAK 5-21-2020

    url = "/sensors"
    basicSensorData = nsmapi.call(url)

    for s in basicSensorData["SensorDescriptor"]:
        sensorId = s["sensorId"]
        sensorName = s["name"]
        idName = f"{sensorId},{sensorName}"
        sensorData[idName] = {}
        for k, v in s.items():
            sensorData[idName][k] = v

    workers = []

    for sensor in sorted(sensorData.keys()):
        # print(sensor)
        thread = threading.Thread(target=sensorDataWorker, args=(sensor, nsmapi, results["startTime"]))
        thread.setName(sensor)
        workers.append(thread)

    numStartingThreads = threading.activeCount()
    for workerThread in workers:
        while True:
            if threading.activeCount() - numStartingThreads > NUMWORKERS:
                print(f"Waiting, {threading.activeCount() - numStartingThreads} Active Threads")
                time.sleep(.3)
            else:
                # print(f"Starting {workerThread}")
                workerThread.setDaemon(True)
                workerThread.start()
                workerThread.join(.1)
                break

    print("All Started")
    timeOutStartTime = time.time()
    while threading.activeCount() - numStartingThreads != 0:
        #TODO need to put a timeout in the config
        if (time.time() - timeOutStartTime) > 180:
            print("Timeout waiting for sensor threads")
            break
        else:
            print(f"Waiting on {threading.activeCount() - numStartingThreads} thread(s) to finish")
            time.sleep(.5)

    print(threading.activeCount() - numStartingThreads)

    return sensorData
