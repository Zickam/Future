import os
import subprocess
import json
import requests

def updateOffsets():
    try:

        link_to_config_file = "https://raw.githubusercontent.com/frk1/hazedumper/master/config.json"
        response = requests.get(link_to_config_file)

        with open("config.json", "w") as f:
            f.write(response.text)

        subprocess.call("Offsets/hazedumper-v2.4.1.exe")

        with open("csgo.json") as file:
            json_data = json.load(file)
            signatures = json_data["signatures"]
            netvars = json_data["netvars"]

        with open("offsets.py", "w") as file:
            file.write("")

        with open("offsets.py", "a") as file:
            for i in signatures:
                file.write("{} = {}\n".format(i, hex(signatures[i])))

            for i in netvars:
                file.write("{} = {}\n".format(i, hex(netvars[i])))

        tmp_1 = os.path.join(os.getcwd(), "csgo.hpp")
        if os.path.isfile(tmp_1):
            os.remove(tmp_1)

        tmp_1 = os.path.join(os.getcwd(), "csgo.cs")
        if os.path.isfile(tmp_1):
            os.remove(tmp_1)

        tmp_1 = os.path.join(os.getcwd(), "csgo.json")
        if os.path.isfile(tmp_1):
            os.remove(tmp_1)

        tmp_1 = os.path.join(os.getcwd(), "csgo.min.json")
        if os.path.isfile(tmp_1):
            os.remove(tmp_1)

        tmp_1 = os.path.join(os.getcwd(), "csgo.toml")
        if os.path.isfile(tmp_1):
            os.remove(tmp_1)

        tmp_1 = os.path.join(os.getcwd(), "csgo.vb")
        if os.path.isfile(tmp_1):
            os.remove(tmp_1)

        tmp_1 = os.path.join(os.getcwd(), "csgo.yaml")
        if os.path.isfile(tmp_1):
            os.remove(tmp_1)

        return "Offsets updated"

    except Exception as _ex:
        return "ERROR", _ex
