import os
import json
import random
import time
from pprint import pprint
import inspect
import datetime
import traceback

def getData(nsmapi, url, resource, startTime):
    #TODO error counter
    # print(url, resource)
    reply = nsmapi.call(url)
    if type(reply) != dict:
        print("Reply is not a dict...that's an error")
        print("Reply:")
        print(reply)
        return {"errorLocal": "bad api reply"}

    try:
        keys = reply.keys()
        if "errorMessage" in keys or "errorId" in keys or "errorLocal" in keys:
            output = f"{url}, ||, {resource}, {reply}"
            with open(f"apiErrors.txt-{startTime}", "a") as of:
                of.write(output)
                of.write("\n")
            # print("-----------")
            # print("error")
            # print(output)
            # print("-----------")
    except:
        print("couldn't find any keys")
        print(reply)

    return reply
