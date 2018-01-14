from robobrowser import RoboBrowser
import random
from plebnet.vpn import config
import sys
import re

class earthvpn:
    headers = config.headers
    h = headers[random.randrange(len(headers))]
    br = RoboBrowser(parser='html.parser', history=True, user_agent=h)
    email = config.earthvpn_username
    password = config.earthvpn_password

    def __init__(self):
        pass

    def login(self, browser=br, link=None):
        # When logging in during purchase, you have to follow the link given, not the standard link.
        if link is None:
            websitelogin = "https://www.earthvpn.com/billing/clientarea.php"
        else:
            websitelogin = link

        browser.open(websitelogin)
        form = browser.get_form(action="dologin.php")
        form['username'].value = self.email
        form['password'].value = self.password
        browser.submit_form(form)

    def purchase(self, currency="ETH", billingcycle=config.earthvpn_billingcycle):
        # Opens the page for the plans.
        website_earthvpn = "https://www.earthvpn.com/billing/cart.php"
        a = self.br.open(website_earthvpn)
        self.br.session.headers['Referer'] = self.br.url

        # Finds the form for the plan.
        form = self.br.get_form(action="/billing/cart.php?a=add&pid=3")
        form["billingcycle"].value = billingcycle
        self.br.submit_form(form)

        # Choosing configurable options, vpn username and vpn password.
        form = self.br.get_forms()[0]
        if config.earthvpn_additionalconnection:
            form['configoption[5]'].value = "8"
        if config.earthvpn_ssl:
            form['configoption[6]'].value = "10"
        if config.earthvpn_staticip:
            form['configoption[4]'].value = "6"
        if config.earthvpn_sshtunnel:
            form['configoption[3]'].value = "4"
        if config.earthvpn_portforwarding:
            form['configoption[9]'].value = "16"
        form['customfield[1]'].value = config.earthvpn_vpnusername
        form['customfield[2]'].value = config.earthvpn_vpnpassword
        form['customfield[20]'].value = config.earthvpn_vpnpassword
        self.br.submit_form(form)

        # Going to the checkout
        page = self.br.parsed
        link = self.br.get_link(text="Checkout")
        self.br.follow_link(link)

        # Logs in.
        page = self.br.parsed
        login_link = self.br.get_link(text="Click here to login")
        if login_link is not None:
            login_link = "https://www.earthvpn.com" + str(login_link).split('"')[1]
            self.login(link=login_link)

        # Choosing payment option and accepting the Terms of Service.
        form = self.br.get_forms()[1]
        form['paymentmethod'].value = "coinpayments"
        form['accepttos'].value = ['on']
        self.br.submit_form(form)

        # Continues to the coinpayments.net platform.
        form = self.br.get_forms()[1]
        self.br.submit_form(form)

        # Choosing the correct currency
        form = self.br.get_form()
        form['selcoin'] = currency
        form['checkout'] = "1"
        form['first_name'] = "Chicker"
        form['email'] = config.earthvpn_username
        self.br.submit_form(form)

if __name__ == '__main__':
    e = earthvpn()
    #e.login()
    e.purchase()

