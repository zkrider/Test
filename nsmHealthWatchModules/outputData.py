import traceback
from pprint import pprint
import json
from nsmHealthWatchModules.getData import getData
import os

def generateOutputsResultDictOnly(results):
    os.chdir(".temp")

    for k, v in results.items():
        print(k)
        try:
            with open(f"{k}.json", "w") as of:
                json.dump(v, of, indent=8)
        except Exception as e:
            traceback.print_exc()
            with open(f"{k}.exception", "w") as of:
                of.write(traceback.format_exc())

    os.chdir("..")

    try:
        with open("specificOutput.json", "w") as of:
            json.dump(results, of, indent=8)
    except:
        traceback.print_exc()

    # with open("specificOutput.json", "w") as of:
    #     json.dump(results, of, indent=8)
    #
def generateFullOutput(results):
    with open("specificOutputFull.json", "w") as of:
        json.dump(results, of, indent=8)

    with open("specificOutput-templateDiff.json", "w") as of:
        json.dump(results["templateDiff"], of, indent=8)




def processOutputs():
    with open("specificOutput.json", "w") as inf:
        results = json.load(inf)

    pprint(results)

if __name__ == "__main__":
    processOutputs()