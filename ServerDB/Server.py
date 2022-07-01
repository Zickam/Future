import psycopg2
import time
import socket
import os
from Modules.Generator import Generator

user = "postgres"
database_name = "futuredb"
user_pass = "25S117200s25@"
main_table_name = "users"
host = "185.87.51.245"
port = 8001

sock = socket.socket()
sock.bind((host, port))
sock.listen(10)


def CurrentTime():
    return int(time.time())
    
def CalculateTimeLicenseExpire(time_paid):

    time_for_license_to_be_active_seconds = 60 * 60 * 24 * 30
    
    time_license_expire = time_for_license_to_be_active_seconds + time_paid

    return time_license_expire

def ConnDefault():
    conn = psycopg2.connect(dbname=database_name, user=user, host="185.87.51.245", password=user_pass, port='5432')
    conn.autocommit = True

    return conn
    
def CheckIfUserExistsLocal(login_hashed):

    conn = ConnDefault()

    with conn.cursor() as cur:
        cur.execute(f"SELECT login_hashed FROM {main_table_name} WHERE login_hashed = %s", (login_hashed,))
        acc = cur.fetchone()
        if acc and len(acc) > 0:
            return True

    return False
    
def CreateNewUser():
    login = input("Login: ")
    password = input("Password: ")
    login_hashed = Generator(login)
    password_hashed = Generator(password)
    current_time = CurrentTime()
    time_paid = CurrentTime()
    time_license_expire = CalculateTimeLicenseExpire(time_paid)
  
    if not CheckIfUserExistsLocal(login_hashed):
      conn = ConnDefault()
      with conn.cursor() as curs:
          curs.execute(f"""INSERT INTO {main_table_name} (login_hashed, password_hashed, time_paid, time_license_expire, time_joined) VALUES ('{login_hashed}', '{password_hashed}', '{time_paid}',  '{time_license_expire}','{current_time}')""")
  
      print("User added")
      
    else:
      print("User already exist!")
    
def FetchUserTimeLicenseExpire():
    login_hashed = conn.recv(2048)
    login_hashed = str(login_hashed)[2:-1]

    conn_bd = ConnDefault()

    with conn_bd.cursor() as curs:
        curs.execute(f"""SELECT time_license_expire FROM {main_table_name} WHERE login_hashed = %s""",
                     (login_hashed,))

        result = curs.fetchone()
        if result and len(result) > 0:
            conn.send(bytes(str(result[0]), "utf-8"))
            return

    conn.send(b'0')

def CheckIfUserExists():
    login_hashed = conn.recv(2048)
    login_hashed = str(login_hashed)[2:-1]

    conn_bd = ConnDefault()

    with conn_bd.cursor() as cur:
        cur.execute(f"SELECT login_hashed FROM {main_table_name} WHERE login_hashed = %s", (login_hashed,))
        acc = cur.fetchone()
        if acc and len(acc) > 0:
            conn.send(b'1')
            return

    conn.send(b'0')

def CheckIfPasswordIsCorrect():
    login_hashed = conn.recv(2048)
    conn.send(b'1')
    login_hashed = str(login_hashed)[2:-1]
    password_hashed = conn.recv(2048)
    password_hashed = str(password_hashed)[2:-1]

    conn_bd = ConnDefault()

    with conn_bd.cursor() as cur:
        cur.execute(f"SELECT * FROM {main_table_name} WHERE login_hashed = %s AND password_hashed = %s",
                    (login_hashed, password_hashed))
        res = cur.fetchone()
        if res and len(res) > 0:
            conn.send(b'1')
            return

    conn.send(b'0')
    
while True:
    conn, addr = sock.accept()
    FuncToCall = conn.recv(1024)

    if FuncToCall:
        print(conn, addr, FuncToCall)
        conn.send(b'1')
        Funcs = dict(globals())
        Func = Funcs[str(FuncToCall)[2:-1]]
        Func()
    conn.close()
