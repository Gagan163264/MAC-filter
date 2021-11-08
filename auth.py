from macfilter import *
import sys
import getpass

pwdf = "pwd.txt"

def loadpwd():
    pwdf = "pwd.txt"
    try:
        with open(pwdf, 'r') as file:
            #config = json.loads(file.read())
            config = json.loads(decrypt(file.read()))
    except IOError:
        config = {}
    return config

def store_data(config):
    with open(pwdf, 'w') as file:
        #file.write(json.dumps(config))
        file.write(encrypt(json.dumps(config)))

pwd=loadpwd()
while True:
    luname = input("Enter admin username: ")
    pword = getpass.getpass('Enter admin password:')

    if luname in pwd.keys():
        if pwd[luname][0] == pword and pwd[luname][1]=='A':
            break
while True:
    var = input("USER MANAGER\n1)Add user\n2)Delete user\n3)View Records\n4)Change Password\n5)Exit\nEnter selection: ")
    if var == '1':
        while True:
            uname = input("Enter new username: ")
            if uname not in pwd.keys():
                break
            print('Name already exists, retry\n')
        type = input("Enter account type(A-admin, U-user):")
        type = type.upper()
        while True:
            pword = getpass.getpass("Enter new password: ")
            cpwrd = getpass.getpass("Confirm password: ")
            if pword == cpwrd and (type == 'A' or type == 'U'):
                break
        pwd[uname]=[pword, type]

    elif var == '2':
        while True:
            uname = input("Enter username to delete: ")
            pword = getpass.getpass('Enter admin password:')
            if uname in pwd.keys() and uname != luname and pword==pwd[luname][0]:
                pwd.pop(uname)
                break
            else:
                print("Username doesnt exist or is currently logged in")

    elif var == '3':
        print("\nDisplaying records:")
        for uname in pwd.keys():
            print(uname,"("+pwd[uname][1]+")")

    elif var == '4':
        while True:
            uname = input("Enter username to change: ")
            prepword = getpass.getpass('Enter previous password:')
            if uname in pwd.keys() and uname != luname and pwd[uname][0] == prepword:
                pword = getpass.getpass("Enter new password: ")
                if pword == getpass.getpass("Confirm password: "):
                    pwd[uname][0]=pword
                break
            else:
                print("Username doesnt exist, is currently logged in or incorrect previous password")

    elif var == '5':
        break
    else:
        print("Invalid Command")
store_data(pwd)
