#!/bin/bash

job="@daily python3 $HOME/git/BlockchainLife/plebnet/vpn/mullvad.py check"

echo $job | crontab - 


