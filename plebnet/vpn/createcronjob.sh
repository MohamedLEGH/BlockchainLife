#!/bin/bash

job="@daily python3 $HOME/git/BlockchainLife/plebnet/vpn/vpncheck.py"

echo $job | crontab - 


