# https://www.vps.ag/lightkvm
from robobrowser import RoboBrowser
import random
from plebnet.vpn import config
import sys
import re

class routerhosting:
    headers = config.headers
    h = headers[random.randrange(len(headers))]
    br = RoboBrowser(parser='html.parser', history=True, user_agent=h)
    username = config.routerhosting_username
    password = config.routerhosting_password


    def __init__(self):
        pass

    def login(self, browser=br, link=None):
        # When logging in during purchase, you have to follow the link given, not the standard link.
        if link is None:
            websitelogin = "https://support.routerhosting.com/clientarea.php"
        else:
            websitelogin = link

        browser.open(websitelogin)
        form = browser.get_form(action="https://support.routerhosting.com/dologin.php")
        form['username'].value = self.username
        form['password'].value = self.password
        browser.submit_form(form)

        print(self.br.parsed)


    def purchase(self, currency="ETH"):
        self.login

        # Opens the page for the plans.
        website_vpsag = "https://support.routerhosting.com/cart.php?a=add&pid=114"
        a = self.br.open(website_vpsag)
        self.br.session.headers['Referer'] = self.br.url

        #print(self.br.parsed)
        for f in self.br.get_forms():
            print(f)

        form = self.br.get_form()
        form['hostname'].value = "ChickerChicker"
        form['configoption[46]'].value = "365"
        form['configoption[40]'].value = "255"
        # print(form.action)
        link = self.br.get_link("View Cart")
        print(str(link))

        sys.exit()

        self.br.submit_form(form)

        print(self.br.parsed)
        for f in self.br.get_forms():
            print(f)

if __name__ == '__main__':
    r = routerhosting()
    #r.login()
    r.purchase()

