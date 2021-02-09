#
# tado_owda.py (Open Window Detection Assist for Tado)
# Created by Adrian Slabu <adrianslabu@icloud.com> on 07.02.2021
# 

import sys
import time

from PyTado.interface import Tado

def login():

    global t
    try:
        t = Tado('your_username@mail.com', 'your_password')

    except Exception as e:
        print (e)
        if (str(e).find("ConnectionError") != -1):
            print ("Connection Error, retrying in 30 sec..")
            time.sleep(30)
            login()
        else:
            print ("Login error.")
            sys.exit(0)

def checkWindowsState():

    try:
        for z in t.getZones():
            zoneID = z["id"]
            zoneName = z["name"]
            if (t.getOpenWindowDetected(zoneID)["openWindowDetected"] == True):
                print (zoneName + ": open window detected, activating the OpenWindow mode.")
                t.setOpenWindow(zoneID)
                print ("Done!")
                print("Waiting for an open window..")

        time.sleep(5.0)
        checkWindowsState()

    except KeyboardInterrupt:
        print ("Interrupted by user.")
        sys.exit(0)

    except Exception as e:
        print(e)
        if (str(e).find("ConnectionError") != -1):
            print ("Connection Error, retrying in 30 sec..")
    
            time.sleep(30)
            checkWindowsState()

login()
print ("Waiting for an open window..")
checkWindowsState()
