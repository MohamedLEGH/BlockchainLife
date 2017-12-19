import sys
import os
import time
import logging

#assuming --> nl

if len(sys.argv) != int(3):
  sys.exit("\n\n*****\n\nPlease provide the approppriate arguments for the script to run corectly. Example:\n\n <path to mullvad config zip file> <server location>\n\n*******\n")


c_pwd = os.path.dirname(os.path.realpath(__file__))
tempfile = c_pwd + '/iptextfile.txt'

c_logdir = c_pwd + '/log'

if os.path.isfile(c_logdir) == False:
    os.popen('mkdir ' + c_logdir).read()

if os.path.isfile(tempfile) == False:
    os.popen('touch ' + tempfile).read()
    file = open(tempfile,'w')
    tempContent = os.popen('curl https://am.i.mullvad.net').read()
    file.write(tempContent)
    file.close()

dd_dir = sys.argv[1]
ss_loc = sys.argv[2]

cm1 = 'apt-get install openvpn'
cm2 = 'apt-get install unzip'

test = os.popen(cm1).read()
test_ = os.popen(cm2).read()

test1 = os.popen("curl https://am.i.mullvad.net").read()

print "gnome-terminal --working-directory='" + c_pwd + "' --command 'python start-vpn.py " + dd_dir + " " + ss_loc + "'"
teststart = os.popen("gnome-terminal --working-directory='" + c_pwd + "' --command 'python start-vpn.py " + dd_dir + " " + ss_loc + "'").read()

time.sleep(5)

test2 = os.popen("curl https://am.i.mullvad.net").read()

c_logfile = c_logdir + '/teststart.log'
logging.basicConfig(filename=c_logfile,level=logging.DEBUG)
logging.debug("************** Script started ************\n")
logging.debug("************** TEST ! ************\n -: " + test)
logging.debug("************** Compare IPs ************\n -: " + test1 + "-:" + test2)


logging.debug("___________________________________________________\n")
