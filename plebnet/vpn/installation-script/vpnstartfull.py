import sys
import os
import time
import logging

#assuming --> nl

if len(sys.argv) != int(4):
  sys.exit("\n\n*****\n\nPlease provide the approppriate arguments for the script to run corectly. Example:\n\n vpnstartfull <path to start-vpn.py> <path to mullvad config zip file> <server location>\n\n*******\n")

sc_dir = sys.argv[1]
dd_dir = sys.argv[2]
ss_loc = sys.argv[3]

cm1 = 'apt-get install openvpn'
cm2 = 'apt-get install unzip'

test = os.popen(cm1).read()
test_ = os.popen(cm2).read()

test1 = os.popen("curl https://am.i.mullvad.net").read()

print "gnome-terminal --working-directory='" + sc_dir + "' --command 'python start-vpn.py " + dd_dir + " " + ss_loc + "'"
teststart = os.popen("gnome-terminal --working-directory='" + sc_dir + "' --command 'python start-vpn.py " + dd_dir + " " + ss_loc + "'").read()

time.sleep(5)

test2 = os.popen("curl https://am.i.mullvad.net").read()

logging.basicConfig(filename='teststart.log',level=logging.DEBUG)
logging.debug("************** Script started ************\n")
logging.debug("************** TEST ! ************\n -: " + test)
logging.debug("************** Compare IPs ************\n -: " + test1 + "-:" + test2)


logging.debug("___________________________________________________\n")
