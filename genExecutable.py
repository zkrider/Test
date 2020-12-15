from pprint import pprint
import zipfile
import subprocess
from datetime import datetime
import shutil
import os
import PyInstaller.__main__
import time
import glob

def genBundle():
    bundleFileName = "nsmHealthWatch-latest.zip"

    filesToBundle = [
        "nsmHealthWatch-latest.exe",
        "nsmHealthWatch-latest.debug.exe",
        "specificOutputTemplate.json",
        "creds.json",
        "config.json",
        "currentVersions.json",
        "run.ps1",
    ]

    for f in os.listdir("flatTemplates"):
        filesToBundle.append(f"flatTemplates/{f}")

    bundle = zipfile.ZipFile(bundleFileName, "w", compresslevel=9)

    for f in filesToBundle:
        bundle.write(f)

    bundle.close()

    pprint(zipfile.ZipFile(bundleFileName).infolist())
    print(f"{os.stat(bundleFileName).st_size / 1024 / 1024}KB")


def genExe():
    MAKEUPX = False
    # MAKEUPX = True

    """
    https://pyinstaller.readthedocs.io/en/stable/spec-files.html
    https://pyinstaller.readthedocs.io/en/stable/usage.html
    """

    startTimeTT = time.time()
    startTimeDT = str(datetime.fromtimestamp(startTimeTT)).replace(":", "-").replace(" ", "_")
    packageNameTimeTime = f"nsmHealthWatch-{startTimeTT:.3f}".replace(".", "_") + ".exe"
    packageNameDateTime = f"nsmHealthWatch-{startTimeDT[:-3]}".replace(".", "_") + ".exe"

    PyInstaller.__main__.run([
        f"--onefile",
        f"--noconfirm",
        f"--clean",
        f"--nowindowed",
        f"--icon={os.path.join('assets', 'icon.ico')}",
        f"--name=nsmHealthWatch-latest.debug.exe",
        f"--distpath=.",
        f"--runtime-tmpdir=.",
        f"--noupx",
        f"-d=all",
        "main.py"
        #    "pullNSMDataPoints.py"
    ])

    PyInstaller.__main__.run([
        f"--onefile",
        f"--noconfirm",
        f"--clean",
        f"--nowindowed",
        f"--icon={os.path.join('assets', 'icon.ico')}",
        f"--name={packageNameTimeTime}",
        f"--distpath=.",
        f"--runtime-tmpdir=.",
        f"--noupx",
        "main.py"
        #    "pullNSMDataPoints.py"
    ])

    shutil.copy(packageNameTimeTime, packageNameDateTime)
    shutil.copy(packageNameTimeTime, "nsmHealthWatch-latest.exe")

    try:
        os.rmdir("__pycache__")
    except:
        pass

    try:
        os.mkdir("spec")
    except:
        pass

    for f in glob.glob("*.spec"):
        shutil.move(os.path.join(f), os.path.join("spec", f))

    print("Done!")
    #TODO figure out why this thing is so effing big

    print(f"Generated {packageNameTimeTime}")
    print(f"Generated {packageNameDateTime}")
    print(f"Generated nsmHealthWatch-latest.exe")
    print(f"Generated nsmHealthWatch-latest.debug.exe")

    #https://stackoverflow.com/questions/25333537/performance-of-subprocess-check-output-vs-subprocess-call
    #https://docs.python.org/3/library/subprocess.html

    # if __name__ != "__main__":
    #     runGeneratedExe()

    print(f"{os.stat('nsmHealthWatch-latest.exe').st_size / 1024 / 1024}KB")

def generateEXEandBundle():
    genExe()
    genBundle()

if __name__ == "__main__":
    generateEXEandBundle()
    # shouldTest = input("Test Latest Generated Executable? ")
    # if shouldTest != "" and shouldTest.lower()[0] == "y":
    #     runGeneratedExe()
