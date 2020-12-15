import requests
import os
import time
import traceback
import sys
import base64
import json
import requests
from requests.exceptions import ReadTimeout
import datetime
from pprint import pprint, pformat
import atexit
try:
    import curlify
except:
    print("couldn't import curlify")
# from Cryptodome import Random
# from Cryptodome.Cipher import AES

class apiConnector():
    #TODO: Add status tracker

    SPACER = "****************************"
    LOGFILE = "nsmapi.{}.log".format(str(datetime.datetime.now()).split(" ")[0])
    base64EncodedAuthorizedUserSessionString = ""
    USERNAME = ""
    PASSWORD = ""
    DEBUG = False
    HOST = ""

    def __init__(self, USERNAME = "", PASSWORD = "", HOST = "", TIMEOUT = 0, RETRIES = 0, DEBUG = False, REUSESESSION = False):
        # In case of logout failure

        requests.packages.urllib3.disable_warnings()
        atexit.register(self.logOut)

        if USERNAME == "":
            self.USERNAME = ""
        else:
            self.USERNAME = USERNAME

        if PASSWORD == "":
            self.PASSWORD = ""
        else:
            self.PASSWORD = PASSWORD

        if HOST == "":
            self.HOST = ""
        else:
            self.HOST = HOST

        if TIMEOUT == 0:
            self.TIMEOUT = 30
        else:
            self.TIMEOUT = TIMEOUT

        if RETRIES == 0:
            self.RETRIES = 3
        else:
            self.RETRIES = RETRIES

        self.DEBUG = DEBUG

        self.REUSESESSION = REUSESESSION

        self.initAPISession()
        curlString = "echo -e \"\\n\"; curl --insecure -k -s -X DELETE https://{}/sdkapi/session -H 'Accept: application/vnd.nsm.v2.0+json' " \
                     "-H 'Content-Type: application/json' -H 'NSM-SDK-API: {}'; echo -e \"\\n\"".format(self.HOST, self.base64EncodedAuthorizedUserSessionString)
        self.log(curlString)


    def log(self, message):
        if self.DEBUG:
            try:
                pprint(json.loads(message))
            except:
                pprint(message)

        with open(self.LOGFILE, "a") as logFile:
            output = "{} | {}".format(datetime.datetime.now(), message)
            logFile.write(output)
            logFile.write("\n")
            logFile.flush()

    def status(self):
        self.log("Connection status check")
        hbcheck = self.call("/heartbeat")
        if "error" in str(hbcheck) or hbcheck == {}:
            self.log("status check failed")
            return {"apiconnection": "FAIL", "info": hbcheck}
        else:
            self.log("status check succeeded")
            return {"apiconnection": "ESTABLISHED"}

    def logOut(self):
        try:
            if self.REUSESESSION == False:
                response = self.call("/session", method="DELETE")
                if response["return"] != 1:
                    print("LOGOUT FAILURE")
                    self.log("Error Logging Out")
                    return "LOGOUT FAILURE"
                else:
                    if os.path.isfile(".session"):
                        os.remove(".session")
                    self.log("Log Out Successful")
                # print("Successful logout from NSM API")
                return "Successful logout from NSM API"
            else:
                print("Saving session")
                self.log("Saving session")
                return "SESSION SAVED"
        except:
            print("LOGOUT EXCEPTION")
            self.log("LOGOUT EXCEPTION")
            return "LOGOUT EXCEPTION"
        self.log("----------------------------------------")
        return "Successful logout from NSM API"

    def encrypt(self, data):
        #TODO: implement encryption of the session string
        return data

    def decrypt(self, data):
        # TODO: implement decryption of the session string
        return data

    def initAPISession(self):
        if os.path.isfile(".session"):
            with open(".session") as ef:
                self.base64EncodedAuthorizedUserSessionString = self.decrypt(ef.read())
                self.log("------------------------")
                self.log("Reusing previous session")
                self.log("UserSessionString: {}".format(self.base64EncodedAuthorizedUserSessionString))
                hbcheck = self.call("/heartbeat")
                if "error" in hbcheck:
                    print("Reinitializing Session")
                    self.log("HBcheck failed, reinitializing session")
                else:
                    return ""

        self.log("--------------------")
        self.log("Creating API Session")
        userPassString = "{}:{}".format(self.USERNAME, self.PASSWORD)
        base64EncodedUserPassString = base64.encodebytes(bytes(userPassString, 'utf-8')).decode().strip()
        self.log(f"{userPassString}")
        self.log(f"{base64EncodedUserPassString}")


        initHeaders = {
            "Accept" : "application/vnd.nsm.v2.0+json",
            "Content-Type" : "application/json",
            "NSM-SDK-API" : base64EncodedUserPassString
        }

        self.log("Init Headers:\n{}".format(pformat(initHeaders, indent=4)))

        sessionInitRequest = requests.Request()
        sessionInitRequest.method = "GET"
        sessionInitRequest.url = "https://{}/sdkapi/session".format(self.HOST)
        sessionInitRequest.headers = initHeaders
        credsResp = requests.Session().send(sessionInitRequest.prepare(), verify=False, timeout=self.TIMEOUT)
        try:
            creds = json.loads(credsResp.text)
        except:
            creds = {}
            print(credsResp.text)
            print(base64EncodedUserPassString)
            print(base64.decodebytes(bytes(base64EncodedUserPassString, "utf-8")))

        self.log("Base64userpass: {}".format(base64EncodedUserPassString))
        self.log("UserSessionCreds: {}".format(creds))

        self.base64EncodedAuthorizedUserSessionString = base64.encodebytes(bytes("{}:{}".format(creds["session"], creds["userId"]), "utf-8")).decode().strip()
        self.log("UserSessionString: {}".format(self.base64EncodedAuthorizedUserSessionString))

        with open(".session", "w") as ef:
            ef.write(self.encrypt(self.base64EncodedAuthorizedUserSessionString))
            self.log("wrote session string")
        print(f"Successful Login to NSM API ({self.HOST})")

    def call(self, resource, method="GET", message="", verbose=False):
        activeSessionHeaders = {
            "Accept" : "application/vnd.nsm.v2.0+json",
            "Content-Type" : "application/json",
            "NSM-SDK-API" : self.base64EncodedAuthorizedUserSessionString
        }

        sessionRequest = requests.Request()
        sessionRequest.method = method
        sessionRequest.url = "https://{}/sdkapi{}".format(self.HOST, resource)

        self.log(sessionRequest.url)

        sessionRequest.headers = activeSessionHeaders
        if method == "PUT" or method == "POST":
            sessionRequest.data = message

        result = ""
        preppedSession = sessionRequest.prepare()

        if verbose:
            curlString = f"curl -k --location --request {method} {sessionRequest.url}"
            if message != "":
                curlString += "?"
                for k, v in json.loads(message).items():
                    if type(v) == list:
                        for v2 in v:
                            curlString += f"{k}={v2}&"
                    else:
                        curlString += f"{k}={v2}&"
            if curlString[-1] == "&":
                curlString = curlString[:-1]
            for k, v in activeSessionHeaders.items():
                curlString += f" --header '{k}: {v}'"
            pprint(activeSessionHeaders)
            print(curlString)
            # print(curlify.to_curl(preppedSession.request))
            pass


        for retry in range(self.RETRIES):
            try:
                result = requests.Session().send(preppedSession, verify=False, timeout=self.TIMEOUT).text
                self.log(result)
                break
            except ReadTimeout:
                print("Retrying {}".format(retry + 1))
                self.log("Retrying {}".format(retry + 1))
                continue
            except Exception as e:
                traceback.print_exc()
                result = json.dumps({"error": e})

        try:
            returnValue = json.loads(result)
        except json.JSONDecodeError:
            returnValue = result
        except Exception as e:
            try:
                returnValue = {"error": str(e), "res": str(result)}
            except:
                returnValue = {"error": str(e), "res": result}
        return returnValue
