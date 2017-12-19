import sys
import os
import datetime
import logging

now = datetime.datetime.now()

toCompare = ""
s_status = ""

fpath = '~/Desktop/textfile.txt'

print(len(sys.argv))

if len(sys.argv) == int(2):
    fpath = sys.argv[1]
    print("sdfsdfsdf: " + fpath)
print(fpath)

if os.path.isfile(fpath):
    file = open(fpath,'r')
    toCompare = file.read()
    file.close()
else:
    s_status = s_status + "\nFILE NOT FOUND\n"

currentIP = os.popen('curl https://am.i.mullvad.net').read()

if toCompare == "":
    s_status = s_status + "\nintitial file containing ip not in " + fpath + "\n"
elif currentIP == toCompare:
    s_status = s_status + "\nvpn on\n"
else:
    s_status = s_status + "\nvpn off\n"


logstatus = "\n_________________________________________\n\n -----" + now.strftime("%Y-%m-%d %H:%M") +  " -----\n\n" + s_status + "\n_______________________________________\n"

logging.basicConfig(filename='vpnStatus.log',level=logging.DEBUG)
logging.debug("************** Vpn status check on " + now.strftime("%Y-%m-%d %H:%M") + " ************\n" + logstatus)
logging.debug("*****************************************")
