import psycopg2
from psycopg2 import sql
import time
from Modules.Generator import Generator
database_name = "futuredb"
user_pass = "25S117200s25@"
main_table_name = "users"
host = "185.87.51.245"
user = "postgres"

def CurrentTime():
    return int(time.time())
    
def CalculateTimeLicenseExpire(time_paid):

    time_for_license_to_be_active_seconds = 60 * 60 * 24 * 30
    
    time_license_expire = time_for_license_to_be_active_seconds + time_paid

    return time_license_expire
    
def Server():

    def ConnDefault():

        conn = psycopg2.connect(dbname=database_name, user=user, host=host, password=user_pass, port="5432")
        conn.autocommit = True

        return conn

    def CreateDatabase():

        loc_conn = psycopg2.connect(user=user, host=host, password=user_pass, port="5432")
        loc_conn.autocommit = True

        with loc_conn.cursor() as cur:
            cur.execute("CREATE DATABASE {}".format(database_name))
            print("Database {} created".format(database_name))

        loc_conn.close()

    def DeleteDatabase():

        loc_conn = psycopg2.connect(user=user, host=host, password=user_pass, port="5432")
        loc_conn.autocommit = True

        with loc_conn.cursor() as cur:
            cur.execute("DROP DATABASE {} WITH (FORCE)".format(database_name))
            print("Database {} deleted".format(database_name))

        loc_conn.close()

    def CreateMainTable():

        conn = ConnDefault()

        with conn.cursor() as curs:
            curs.execute(f"""CREATE TABLE {main_table_name}(
                id SERIAL PRIMARY KEY,
                login_hashed VARCHAR(255) NULL,
                password_hashed VARCHAR(255) NULL,
                time_paid INT NULL,
                time_license_expire INT NULL,
                time_joined INT NULL
            )
                    """)
            print(f"Table {main_table_name} created")

        conn.close()

    def DeleteMainTable():

        conn = ConnDefault()

        with conn.cursor() as curs:
            curs.execute(f"""DROP TABLE {main_table_name}
                    """)
            print(f"Table {main_table_name} deleted")

        conn.close()

    def AddUser(login_hashed, password_hashed, current_time):

        # execute only first time user is registrated
        # should be very secure

        conn = ConnDefault()

        # cur = conn.cursor()
        # cur.execute(
        #     sql.SQL("""INSERT INTO {0} ({1}, {2}, {3}) VALUES ({4}, {5}, {6})""".format(sql.Identifier('users'),
        #                                                                                                               sql.Identifier('login_hashed'),
        #                                                                                                               sql.Identifier('password_hashed'),
        #                                                                                                               sql.Identifier('time_joined'),
        #                                                                                                               sql.Identifier(login_hashed),
        #                                                                                                               sql.Identifier(password_hashed),
        #                                                                                                               sql.Identifier(current_time)
        #                                                                                                               )))

        # query = sql.SQL("select {field} from {table} where {pkey} = %s").format(
        #     field=sql.Identifier('my_name'),
        #     table=sql.Identifier('some_table'),
        #     pkey=sql.Identifier('id'))

        # query = sql.SQL("INSERT INTO {table_name} ({row_1}, {row_2}, {row_3}) VALUES ({value_for_row_1, value_for_row_2, value_for_row_3})").format(
        #     table_name=sql.Identifier(main_table_name),
        #     row_1=sql.Identifier('login_hashed'),
        #     row_2=sql.Identifier('password_hashed'),
        #     row_3=sql.Identifier('time_joined'),
        #     value_for_row_1=sql.Identifier(login_hashed),
        #     value_for_row_2=sql.Identifier(password_hashed),
        #     value_for_row_3=sql.Identifier(current_time)
        # )

        # cur.execute(query, (42,))



        with conn.cursor() as curs:
            curs.execute(f"""INSERT INTO {main_table_name} (login_hashed, password_hashed, time_joined) VALUES ('{login_hashed}', '{password_hashed}', '{current_time}')""")

        print("User added")

        conn.close()

    def RecreateAll():

        # DeleteMainTable()
        DeleteDatabase()
        CreateDatabase()
        CreateMainTable()

        print("Recreated")
        
    def FetchAllUsersData():

        conn = ConnDefault()
        with conn.cursor() as curs:
            curs.execute(f"""SELECT * FROM {main_table_name}""")
            result = curs.fetchall()
        return result
        
    def CheckIfUserExists(login_hashed):

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

        if not CheckIfUserExists(login_hashed):
          conn = ConnDefault()
          with conn.cursor() as curs:
              curs.execute(f"""INSERT INTO {main_table_name} (login_hashed, password_hashed, time_paid, time_license_expire, time_joined) VALUES ('{login_hashed}', '{password_hashed}', '{time_paid}',  '{time_license_expire}','{current_time}')""")

          print("User added")
          
        else:
          print("User already exist!")

    try:
        # RecreateAll()
        # AddUser(hashed_active_account, password_hashed, current_time)
        # print(FetchAllUsersData())
        CreateNewUser()



        print("[INFO] Server has been shut downed")

    except Exception as _ex:
        print("[Error]", _ex)

Server()