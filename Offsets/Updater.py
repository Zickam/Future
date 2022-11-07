import os
import subprocess
import json
import sys

import requests

offsets_file = "Offsets/offsets.py"
files_to_delete = ["csgo.hpp", "csgo.cs", "csgo.json", "csgo.min.json", "csgo.toml",
                   "csgo.vb", "csgo.yaml", "hazedumper.log"]

def addOffsetsFolderToPath():
    sys.path.append(f"{os.getcwd()}\\Offsets\\hazedumper-v2.4.1.exe")


def updateOffsets():
    try:

        link_to_config_file = "https://raw.githubusercontent.com/frk1/hazedumper/master/config.json"
        response = requests.get(link_to_config_file)

        with open("Offsets/config.json", "w") as f:
            f.write(response.text)

        subprocess.call(f"Offsets/hazedumper-v2.4.1.exe")

        with open("csgo.json") as file:
            json_data = json.load(file)
            signatures = json_data["signatures"]
            netvars = json_data["netvars"]

        with open(offsets_file, "w") as file:
            file.write("")

        with open(offsets_file, "a") as file:
            for i in signatures:
                file.write("{} = {}\n".format(i, hex(signatures[i])))

            for i in netvars:
                file.write("{} = {}\n".format(i, hex(netvars[i])))

        for _ in files_to_delete:
            _ = os.path.join(os.getcwd(), _)
            if os.path.isfile(_):
                os.remove(_)

        return True

    except Exception as _ex:
        return "ERROR", _ex
