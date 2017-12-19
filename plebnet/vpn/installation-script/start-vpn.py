import sys
import os
import logging

#assuming --> nl

test1 = os.popen("curl https://am.i.mullvad.net").read()

#current = 'nl'
ddir = sys.argv[1]
current = sys.argv[2]
#ddir = '~/Desktop/vontest/mullvad_config_linux_nl.zip';
confdir = ddir.split(".")[0]

#unzip the file to the confdir
temp = ddir.split("/")
del temp[-1]
unzdir = '/'.join(temp)

cm2 = 'unzip -o ' + ddir + ' -d ' + unzdir


cmmnd1 = 'cp ' + confdir + '/* ./.'
cmmnd2 = 'nohup openvpn --config ./mullvad_' + current + '.conf > /dev/null'

output_cm2 = os.popen(cm2).read()
output1 = os.popen(cmmnd1).read()
output2 = os.popen(cmmnd2).read()

test2 = os.popen("curl https://am.i.mullvad.net").read()

logging.basicConfig(filename='test.log',level=logging.DEBUG)
logging.debug("*********** Downloaded file location *************\n\n" + ddir + "\n")

logging.debug("*********** Extracted file to *************\n\n" + confdir +  "\n")

logging.debug("*********** Copied files to *************\n" + cmmnd1 + " \n")


logging.debug("*********** compare ip *************\n")
logging.debug('- test1: ' + test1 + "\n")
logging.debug('- test2: ' + test2 + "\n")
logging.debug("************************************")
logging.debug("**************** file extraction *********************\n")
logging.debug("- cm2: \n" + output_cm2 + "\n")
logging.debug("******************************************************")

logging.debug('output1: ' + output1)
logging.debug('output2: ' + output2)
