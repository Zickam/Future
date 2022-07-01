import sys
import subprocess
import os

missingpackages = []
string = ""
def installerfunction():
    print("---Checking Modules---")
    global missingpackages, string
    try:
        import pymem
        print(pymem.__name__)
    except ImportError:
        missingpackages.append("pymem")

    try:
        import keyboard
        print(keyboard.__name__)
    except ImportError:
        missingpackages.append("keyboard")

    try:
        import pygame
        print(pygame.__name__)
    except ImportError:
        missingpackages.append("pygame")

    try:
        import threading
        print(threading.__name__)
    except ImportError:
        missingpackages.append("threading")

    try:
        import requests
        print(requests.__name__)
    except ImportError:
        missingpackages.append("requests")

    try:
        import mouse
        print(mouse.__name__)
    except ImportError:
        missingpackages.append("mouse")

    try:
        import time
        print(time.__name__)
    except ImportError:
        missingpackages.append("time")

    try:
        import datetime
        print(datetime.__name__)
    except ImportError:
        missingpackages.append("datetime")

    try:
        import pynput
        print(pynput.__name__)
    except ImportError:
        missingpackages.append("pynput")

    try:
        import numpy
        print(numpy.__name__)
    except ImportError:
        missingpackages.append("numpy")

    try:
        import pywintypes
        print(pywintypes.__name__)
    except ImportError:
        missingpackages.append("pywin32")



    # if all packages are installed
    if len(missingpackages) == 0:
        print("All packages have been installed, continuing..")
        print("----------------------------------------------")
        os.system("cls")

    # if some packages are missing
    if len(missingpackages) > 0:
        for element in range(0, len(missingpackages)):
            string += missingpackages[element]
            if element < len(missingpackages)-1:
                string += ", "

        print("You are missing ["+string+"]")
        if input("Do you want to install? >").upper() == "Y":
            for element in range(0, len(missingpackages)):
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', str(missingpackages[element])])

