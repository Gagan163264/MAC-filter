
import json
import os
import sys
import datetime

dfile = 'str.txt'
dumpfile = 'dump.txt'


#macfile = '/etc/dnsmasq.d/03-custom-DHCP.conf'
macfile = 'macfile.txt'

def write_dump(str1):
    with open(dumpfile, "a") as dfile:
        dfile.write(str1)

def loadconfig():
    try:
        with open(dfile, 'r') as file:
            #config = json.loads(file.read())
            config = json.loads(decrypt(file.read()))
    except IOError:
        config = {}
    return config

def store_data(config):
    with open(dfile, 'w') as file:
        #file.write(json.dumps(config))
        file.write(encrypt(json.dumps(config)))

def decrypt(str1):
    strn = ""
    counter = 0;
    for strg in str1.split("\n"):
        for chrt in strg.split(" "):
            if chrt != "":
                strn+=str(chr(int(chrt)-counter))
                counter += 1
                if(counter>1000):
                    counter = 0
        strn+="\n"
    return strn[:-1]

def encrypt(str1):
    strn = ""
    counter = 0;
    for chr in str1:
        if chr != "\n":
            strn += str(ord(chr)+counter)+" "
            counter += 1
            if(counter>1000):
                counter = 0
        else:
            strn+="\n"
    return strn

def addMAC(data):
    config = loadconfig()
    name = data[2]
    phonenum = data[0]
    MAC = data[1]
    nmon = int(data[3])
    date = datetime.datetime.today().strftime('%d-%m-%Y')
    addstr = 'dhcp-host='+MAC+',set:known\n'
    if phonenum in config.keys():
        mac = config[phonenum][0]
    else:
        mac = {}
    #dt = datetime.datetime.now() + datetime.timedelta(30)*nmon
    #mac[MAC] = dt.strftime('%d-%m-%Y')
    if MAC in mac.keys():
        return 0
    mac[MAC] = [nmon, date]
    config[phonenum]=[mac, name]
    with open(macfile, "a") as omacfile:
        omacfile.write(addstr)
    write_dump("Add||"+name+"||"+phonenum+"||"+MAC+"||"+str(nmon)+"||"+date+"\n")
    store_data(config)
    return 1

def displayMAC():
    config = loadconfig()
    if not config:
        return "No data stored"
    strn = ''
    for phn in config:
        strn += "Phone Number: "+str(phn)+"\n"
        strn += "Name: "+str(config[phn][1])+"\n"
        strn += "MACs registered:\n"
        for mac in config[phn][0]:
            if mac == 0:
                continue
            strn += mac+"\n"
            nmon = int(config[phn][0][mac][0])
            if nmon == 0:
                strn+="MAC disabled"
            else:
                dreg = datetime.datetime.strptime(config[phn][0][mac][1], '%d-%m-%Y')
                dt = dreg + datetime.timedelta(30)*nmon
                dt = dt.strftime('%d-%m-%Y')
                strn += str(config[phn][0][mac][1])+" to "+dt +"("+str(config[phn][0][mac][0])+" months)\n\n"
        strn+= "\n\n\n"
    return strn

def delMAC(data):
    config = loadconfig()
    MAC = data[1]
    phonenum = data[0]
    write_dump("Delete||"+config[phonenum][1]+"||"+phonenum+"||"+MAC+"||"+str(config[phonenum][0][MAC][0])+"||"+config[phonenum][0][MAC][1]+"\n")
    if phonenum not in config.keys():
        return 0
    mac = config[phonenum][0]
    if MAC not in mac:
        return 0
    mac.pop(MAC)
    if len(mac)==0:
        config.pop(phonenum)
    addstr = 'dhcp-host='+MAC+',set:known\n'
    with open(macfile, "r") as omacfile:
        str = omacfile.read()
    str = str.replace(addstr, '')
    with open(macfile, "w") as omacfile:
        str = omacfile.write(str)
    store_data(config)
    return 1

def updateMAC(data):
    config = loadconfig()
    MAC = data[1]
    phonenum = data[0]
    nmonnew = int(data[2])
    if phonenum not in config.keys():
        return 0
    mac = config[phonenum][0]
    if MAC not in mac:
        return [0,0]
    dreg = datetime.datetime.strptime(config[phonenum][0][MAC][1], '%d-%m-%Y')
    dt = dreg + datetime.timedelta(30)*int(config[phonenum][0][MAC][0])
    deltav = datetime.datetime.today()-dt
    delv = int(deltav.days)
    print(deltav)
    nmon = config[phonenum][0][MAC][0]
    if nmonnew<=nmon:
        if nmonnew > (-1*delv)//30:
            return [-1,0]
    config[phonenum][0][MAC][0]=nmonnew
    store_data(config)
    write_dump("update||"+config[phonenum][1]+"||"+phonenum+"||"+MAC+"||"+str(config[phonenum][0][MAC][0])+"||"+config[phonenum][0][MAC][1]+"\n")
    return [1,nmonnew-nmon]

def cleaner():
    config = loadconfig()
    date = datetime.datetime.today().strftime('%d-%m-%Y')
    print("Event trigerred on ", date)
    for phn in config:
        for mac in config[phn][0]:
            dreg = datetime.datetime.strptime(config[phn][0][mac][1], '%d-%m-%Y')
            dt = dreg + datetime.timedelta(30)*int(config[phn][0][mac][0])
            dt = dt.strftime('%d-%m-%Y')
            if dt==date:
                config[phn][0][mac][0]=0
                store_data(config)
                write_dump("Auto-disabled||"+config[phn][1]+"||"+phn+"||"+MAC+"||"+str(config[phn][0][mac][0])+"||"+config[phn][0][mac][1]+"\n")
    return 1
