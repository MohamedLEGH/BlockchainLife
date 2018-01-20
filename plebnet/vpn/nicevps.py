from robobrowser import RoboBrowser
import random
from plebnet.vpn import config
import sys
import re

class nicevps:
    headers = config.headers
    h = headers[random.randrange(len(headers))]
    br = RoboBrowser(parser='html.parser', history=True, user_agent=h)
    email = config.nicevps_username
    password = config.nicevps_password

    def __init__(self):
        pass

    def login(self, browser=br, link=None):
        # When logging in during purchase, you have to follow the link given, not the standard link.
        if link is None:
            websitelogin = "https://nicevps.net/login"
        else:
            websitelogin = link

        browser.open(websitelogin)
        form = self.br.get_form(action="https://nicevps.net/login/login")
        form['user'].value = self.email
        form['pass'].value = self.password
        browser.submit_form(form)


    def purchase(self, currency="ETH"):
        self.login()

        # Opens the page for the plans.
        website_earthvpn = "https://nicevps.net/products/configure/VPN_1K"
        a = self.br.open(website_earthvpn)
        self.br.session.headers['Referer'] = self.br.url

        #page = self.br.parsed
        #print(page)

        forms = self.br.get_forms()
        for f in forms:
            print(f)
        form = self.br.get_form()
        form['traffic'].value = config.nicevps_additionaltraffic
        form['ip_type'].value = config.nicevps_iptype
        form['billing_term'].value = config.nicevps_billingcycle
        self.br.session.headers['Referer'] = self.br.url
        self.br.submit_form(form)

        page = self.br.parsed
        print(page)
        forms = self.br.get_forms()

        for f in forms:
            print(f)

if __name__ == '__main__':
    n = nicevps()
    #n.login()
    n.purchase()

