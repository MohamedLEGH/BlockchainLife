# https://www.vps.ag/lightkvm
from robobrowser import RoboBrowser
import random
from plebnet.vpn import config
import sys
import re

class vpsag:
    headers = config.headers
    h = headers[random.randrange(len(headers))]
    br = RoboBrowser(parser='html.parser', history=True, user_agent=h)
    username = config.vpsag_username
    email = config.vpsag_email
    password = config.vpsag_password

    def __init__(self):
        pass

    def login(self, browser=br, link=None):
        # When logging in during purchase, you have to follow the link given, not the standard link.
        if link is None:
            websitelogin = "https://www.vps.ag/login.php"
        else:
            websitelogin = link

        browser.open(websitelogin)
        form = browser.get_form(action="login.php?return=")
        print(form)
        form['user'].value = self.username
        form['pass'].value = self.password
        browser.submit_form(form)


    def purchase(self, currency="ETH"):
        self.login

        # Opens the page for the plans.
        website_vpsag = "https://www.vps.ag/lightkvm"
        a = self.br.open(website_vpsag)
        self.br.session.headers['Referer'] = self.br.url

        form = self.br.get_form()
        # form['billingcycle'].value = config.vpsag_billingcycle # Billing cycle
        # form['os'].value = config.vpsag_os # Operating System
        # form['cpuslider'].value = config.vpsag_cpuslider # Additional CPUs
        # form['ramslider'].value = config.vpsag_ramslider # Additional RAM
        # form['diskslider'].value = config.vpsag_diskslider # Additional Disk Space
        # form['bandwidth'].value = config.vpsag_bandwidth # Bandwidth
        # form['backup'].value = config.vpsag_backup # Backups
        # form['price_monthly'].value = "€3.00"
        # form['price_semianually'].value = "€16.20"
        # form['price_anually'].value = "€28.80"
        print(form.action)
        #form.action = form.action + "&rand=1516109511447"
        print(form.action)
        print(self.br.state)

        self.br.submit_form(form)

        print(self.br.url)
        print(self.br.parsed)

        sys.exit(0)

        # Finds the form for the plan.
        for f in self.br.get_forms():
            print(f)

if __name__ == '__main__':
    v = vpsag()
    #v.login()
    v.purchase()

