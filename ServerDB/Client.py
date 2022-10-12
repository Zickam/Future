import socket
import datetime
import time
import requests

host = "185.87.51.106"
port = 8001

def CheckIfServerOnline():
    try:
        sock = socket.socket()
        sock.connect((host, port))
        return True
    except TimeoutError:
        return "error"
    except ConnectionRefusedError:
        return "error"

def CurrentTime():
    return int(time.time())

def CheckIfUserExists(login_hashed):
    sock = socket.socket()
    sock.connect((host, port))
    sock.send(b"CheckIfUserExists")

    sock.send(bytes(login_hashed, "utf-8"))
    sock.recv(1)

    IsUserExists = sock.recv(1)
    sock.close()

    if (str(IsUserExists)[2:-1] == "1"):
        return True

    return False

def FetchUserTimeLicenseExpire(login_hashed):
    sock = socket.socket()
    sock.connect((host, port))
    sock.send(b"FetchUserTimeLicenseExpire")

    sock.send(bytes(login_hashed, "utf-8"))
    sock.recv(1)

    UserTimeLicenseExpire = sock.recv(1024)
    sock.close()

    return str(UserTimeLicenseExpire)[2:-1]

def TimeZoneOffsetHours():
    now = datetime.datetime.now()
    local_now = now.astimezone()
    local_tz = local_now.tzinfo.utcoffset(local_now)
    hours_offset = ""

    for i in str(local_tz):
        if i == ":":
            break
        else:
            hours_offset += i

    hours_offset = int(hours_offset)
    return hours_offset

def CurrentLocalTime():
    server_for_time = "https://just-the-time.appspot.com/"
    request = requests.get(server_for_time)
    server_time = request.text.split(" ")
    server_time = server_time[0].split("-") + server_time[1].split(":")
    new = []
    for i in server_time:
        new.append(int(i))

    dt = datetime.datetime(new[0], new[1], new[2], new[3], new[4], new[5])
    current_local_time = dt.timestamp() + TimeZoneOffsetHours() * 3600

    return current_local_time

def CheckIfUserLicenseIsValid(login_hashed):
    current_local_time = int(CurrentLocalTime())
    time_license_expire = int(FetchUserTimeLicenseExpire(login_hashed))

    if time_license_expire > current_local_time:
        return True

    else:
        return False

def CheckIfPasswordIsCorrect(login_hashed, password_hashed):
    sock = socket.socket()
    sock.connect((host, port))
    sock.send(b"CheckIfPasswordIsCorrect")
    sock.recv(1)
    sock.send(bytes(login_hashed, "utf-8"))
    sock.recv(1)
    sock.send(bytes(password_hashed, "utf-8"))

    IsPasswordCorrect = sock.recv(1)
    sock.close()

    if (str(IsPasswordCorrect)[2:-1] == "1"):
        return True

    return False