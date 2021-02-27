#
# tado_owda.py (Open Window Detection Assist for Tado)
# Created by Adrian Slabu <adrianslabu@icloud.com> on 07.02.2021
# 

import sys
import time

from PyTado.interface import Tado

def main():

    global lastMessage
    global username
    global password
    global checkingInterval
    global errorRetringInterval

    lastMessage = ""

    username = "your_username" # tado username
    password = "your_password" # tado password

    checkingInterval = 10.0 # checking interval (in seconds)
    errorRetringInterval = 30.0 # retrying interval (in seconds), in case of an error

    login()
    printm ("Waiting for an open window..")
    checkWindowsState()

def login():

    global t

    try:
        t = Tado(username, password)

        if (lastMessage.find("Connection Error") != -1):
            printm ("Connection established, everything looks good now, continuing..")

    except KeyboardInterrupt:
        printm ("Interrupted by user.")
        sys.exit(0)

    except Exception as e:
        if (str(e).find("access_token") != -1):
            printm ("Login error, check the username / password !")
            sys.exit(0)
        else:
            printm (str(e) + "\nConnection Error, retrying in " + str(errorRetringInterval) + " sec..")
            time.sleep(errorRetringInterval) 
            login()

def checkWindowsState():
    i = 0
    while i < 3: # My solution to fix the "stack depth"
        try:
            for z in t.getZones():
                zoneID = z["id"]
                zoneName = z["name"]
                if (t.getOpenWindowDetected(zoneID)["openWindowDetected"] == True):
                    printm (zoneName + ": open window detected, activating the OpenWindow mode.")
                    t.setOpenWindow(zoneID)
                    printm ("Done!")
                    printm ("Waiting for an open window..")

            if (lastMessage.find("Connection Error") != -1):
                printm ("Connection established, everything looks good now, continuing..")
                printm ("Waiting for an open window..")

            time.sleep(checkingInterval)
            checkWindowsState()

        except KeyboardInterrupt:
            printm ("Interrupted by user.")
            sys.exit(0)

        except Exception as e:
            printm (str(e) + "\nConnection Error, retrying in " + str(errorRetringInterval) + " sec..")
            time.sleep(errorRetringInterval)
            checkWindowsState()

def printm(message):
    global lastMessage
    if (message != lastMessage):
        lastMessage = (message)
        sys.stdout.write(message + "\n")

main()
