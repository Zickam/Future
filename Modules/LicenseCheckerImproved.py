import getpass
from hashlib import sha256

local_accounts_path = r"C:\Program Files (x86)\Steam\config\loginusers.vdf"
logins_paid = rf"C:\Users\{getpass.getuser()}\OneDrive\Desktop\Python\Future\license_keys_test.txt"

def Double_SHA256(text):
    return sha256(sha256(text.encode()).hexdigest().encode()).hexdigest()



def LocalAccountsNamesReader():

    with open(local_accounts_path, "r") as file:
        file_content = file.read()
        file_content = file_content.split("\t")

        for i in range(len(file_content)):
            if file_content[i] == '"AccountName"':
                if file_content[i + 26][:-1] == '"1"':
                    account_name = file_content[i + 2]

        account_name = account_name[1:-2]



def paidLogins():

    with open(logins_paid, "r") as file:
        file_content = file.read()
        file_content = file_content.split("\n")

    return file_content

def encryptLogin(login):

    login = login.lower()
    login = Double_SHA256(login)

    return login

def mainChecker():

    paid_logins = paidLogins()
    for i in LocalAccountsNamesReader():
        if encryptLogin(i) in paid_logins:
            return True

    return False

LocalAccountsNamesReader()

