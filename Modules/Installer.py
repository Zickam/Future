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

    try:
        import colorama
        print(colorama.__name__)
    except ImportError:
        missingpackages.append("colorama")

    try:
        import psutil
        print("psutil")
    except ImportError:
        missingpackages.append("psutil")

    try:
        import loguru
        print("loguru")
    except ImportError:
        missingpackages.append("loguru")

    # if all packages are installed
    if len(missingpackages) == 0:
        os.system("cls")
        print("All packages were installed already, continuing...")
        print("----------------------------------------------")

    # if some packages are missing
    elif len(missingpackages) > 0:

        print(f"You are missing {missingpackages}]")
        install = input("Do you want to install? > ")

        if install.lower() == "y" or install[::].lower() == "yes":
            for element in range(0, len(missingpackages)):
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', str(missingpackages[element])])

            os.system("cls")
            print("All packages have been installed, continuing...")
            print("----------------------------------------------")
        else:
            os.system("cls")
            print("You have choosen to not to install missing packages")
            print("Program probably won't work... Launching...")
            print("----------------------------------------------")
