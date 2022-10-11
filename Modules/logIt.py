import datetime
import os
import subprocess
import sys

try:
    import colorama

except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', "colorama"])
    print()
    print("Installed colorama needed for logIt")
    print()

import colorama
from colorama import Fore
from colorama import Style


show_time = False

default_logs_directory = os.path.join("logs")
default_logs_file = os.path.join("logs_default.txt")


def proveExistanceOfFile(file):
    if not os.path.isfile(file):
        with open(file, 'w') as f:
            f.write('1')


def proveExistanceOfFolder(folder):
    if not os.path.isdir(folder):
        os.mkdir(folder)


def currTime():
    return str(datetime.datetime.now())


def consoleLog(text, type):

    type = type.upper()
    curr_time = ""
    color = Fore.YELLOW

    if type == "ERROR" or type == "WARNING":
        color = Fore.RED
    elif type == "START":
        color = Fore.BLUE
    elif type == "IMPORTANT":
        color = Fore.LIGHTRED_EX
    elif type == "DEBUG":
        color = Fore.LIGHTCYAN_EX

    if show_time:
        curr_time = currTime() + " "

    print(f"{curr_time}{color}[{type}]{Style.RESET_ALL}" + " " + str(text))


def writeLog(text, file_to_save_to, type):
    with open(file_to_save_to, "a") as l_file:
        l_file.write(f"{currTime()} [{type.upper()}]" + " " + str(text) + "\n")


def logIt(text, file_to_save_to=default_logs_file, directory_to_save_to=default_logs_directory, type="info"):
    proveExistanceOfFolder(directory_to_save_to)

    full_path_to_save_to = os.path.join(directory_to_save_to, file_to_save_to)
    proveExistanceOfFile(full_path_to_save_to)

    writeLog(text, full_path_to_save_to, type)
    consoleLog(text, type)