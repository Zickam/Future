import os
import time
import psutil
import Modules.Startcsgo
import ctypes  # An included library with Python install.

database_name = "future"
database_pass = "123"
main_table_name = "users"

local_file = "loginuserspath.txt"

def GetActiveAccount():
    with open(findLoginUsers(), "r", encoding="UTF-8") as file:
        file_content = file.read()[9:-3]
        file_content = "\t" + file_content
        file_content_organized = dict()
        is_in = False
        count = 0
        is_key = False
        for i in range(len(file_content)):
            if file_content[i] == "{":
                is_in = True
                is_key = True
                loc_dict = dict()
            elif file_content[i] == "}":
                is_in = False
                count = 0
                is_key = False
                file_content_organized[curr_user_id] = loc_dict

            if is_in:
                if file_content[i:i + 3].encode() == "\n\t\t".encode():
                    is_key = True
                    i_start_key = i + 3
                    count = 0
                elif file_content[i:i + 2].encode() == "\t\t".encode():
                    is_value = True
                    i_start_value = i + 2
                    count = 0

                if file_content[i] == '"':
                    count += 1
                    if count == 2:
                        if is_key:
                            key = file_content[i_start_key + 1:i]
                            is_key = False
                        elif is_value:
                            value = file_content[i_start_value + 1:i]
                            is_value = False
                            loc_dict[key] = value

            else:
                border_right = i
                border_left = i
                while file_content[border_right].encode() != "{".encode() and border_right != len(file_content) - 1:
                    border_right += 1

                while file_content[border_left].encode() != "}".encode() and border_left != 0:
                    border_left -= 1

                curr_user_id = file_content[border_left + 4:border_right - 3]

    user_login = ""

    for user_id, user_info in file_content_organized.items():
        for key, value in user_info.items():
            if key == "MostRecent" and value == "1":
                user_login = file_content_organized[user_id]["AccountName"]

    return user_login

def GetWebHelpersList():
    web_helper_list = []
    for proc in psutil.process_iter():
        pInfoDict = proc.as_dict(attrs=['pid', 'name', 'cpu_percent'])
        if pInfoDict["name"] == "steamwebhelper.exe":
            web_helper_list.append(pInfoDict["pid"])

    return web_helper_list

def CheckValid():

    web_helpers_list = GetWebHelpersList()
    Passed = False

    for element in web_helpers_list:
        unixtime = os.stat(findLoginUsers()).st_mtime
        steamuptime = str(psutil.Process(element)).split("started='")[1].replace("')", "")
        if str(steamuptime) == str(time.strftime('%H:%M:%S', time.localtime(unixtime))):
            Passed = True

    return Passed

def rememberLoginUsers(default_root):
    with open(local_file, "w") as file:
        file.write(default_root)

def checkIfLoginUsersRemembered():
    if os.path.isfile(local_file):
        with open(local_file, "r") as file:
            default_root = file.read()

        if default_root:
            return default_root
        else:
            return False
    else:
        return False

def checkIfLoginUsersCorrectlyRemembered(root):
    if os.path.isfile(root):
        return True
    else:
        return False

def showMessageBox(title, text):
    ctypes.windll.user32.MessageBoxW(0, str(text), str(title), 0)

def findLoginUsersFile():

    default_root, nothing, nothing1 = Modules.startcsgo.GetActiveProcesses()

    return default_root + "loginusers.vdf"

def findLoginUsers():

    root = checkIfLoginUsersRemembered()
    if root:
        res = checkIfLoginUsersCorrectlyRemembered(root)
        if res:
            return root

        else:
            root = findLoginUsersFile()
            rememberLoginUsers(root)
            return root

    else:
        root = findLoginUsersFile()
        rememberLoginUsers(root)
        return root
