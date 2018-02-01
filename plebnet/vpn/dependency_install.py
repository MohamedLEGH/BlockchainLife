import os

#run as root

print("\nstarting dependency installing process....")

#install pip for python 3
print("\ninstalling pip for python 3...\n")
test_ = os.popen('apt-get install -y python3-pip').read()
print(test_)

#install selenium library for python 3
print("\ninstalling selenium for python3....\n")
test_ = os.popen('pip3 install selenium').read()
print(test_)


#install zip
print("\ninstalling zip....\n")
test_ = os.popen('apt-get install -y zip').read()
print(test_)

#install openvpn
print("\ninstalling openvpn....\n")
test_ = os.popen('apt-get install -y openvpn').read()
print(test_)

#install chromedriver
print("\ninstalling chromedriver....\n")
test_ = os.popen('apt-get install -y chromium-chromedriver').read()
print(test_)


