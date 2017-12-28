import sys
import os
import datetime
import logging

now = datetime.datetime.now()

toCompare = ""
s_status = ""

fpath = os.path.dirname(os.path.realpath(__file__)) + '/iptextfile.txt'

c_logdir = os.path.dirname(os.path.realpath(__file__)) + '/log'

if os.path.isfile(c_logdir) == False:
    os.popen('mkdir ' + c_logdir).read()

print(len(sys.argv))

if len(sys.argv) == int(2):
    fpath = sys.argv[1]
    print("custom path: " + fpath)
print("statndar path" + fpath)

if os.path.isfile(fpath):
    file = open(fpath,'r')
    toCompare = file.read()
    file.close()
else:
    s_status = s_status + "\nFILE NOT FOUND\n"

currentIP = os.popen('curl https://am.i.mullvad.net').read()

if toCompare == "":
    s_status = s_status + "\nintitial file containing ip not in " + fpath + "\n"
elif currentIP != toCompare:
    s_status = s_status + "\nvpn on\n"
else:
    s_status = s_status + "\nvpn off\n"


logstatus = "\n_________________________________________\n\n -----" + now.strftime("%Y-%m-%d %H:%M") +  " -----\n\n" + s_status + "\n_______________________________________\n"

c_logfile = c_logdir + '/vpnStatus.log'
logging.basicConfig(filename=c_logfile,level=logging.DEBUG)
logging.debug("************** Vpn status check on " + now.strftime("%Y-%m-%d %H:%M") + " ************\n" + logstatus)
logging.debug("*****************************************")
