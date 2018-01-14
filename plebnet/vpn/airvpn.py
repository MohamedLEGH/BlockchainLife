from robobrowser import RoboBrowser
import random
from plebnet.vpn import config
import sys
import re

class airvpn:
    headers = config.headers
    h = headers[random.randrange(len(headers))]
    br = RoboBrowser(parser='html.parser', history=True, user_agent=h)
    email = config.airvpn_username
    password = config.airvpn_password

    def __init__(self):
        print("This is the constructor")

    def login(self, browser=br, link=None):
        #When loging in during purchase, you have to follow the link given, not the standard link.
        if link is None:
            websitelogin = "https://airvpn.org/index.php?app=core&module=global&section=login"
        else:
            websitelogin = link

        browser.open(websitelogin)
        page = str(browser.parsed)
        form = browser.get_form(action="https://airvpn.org/index.php?app=core&module=global&section=login&do=process")
        form['ips_username'].value = self.email
        form['ips_password'].value = self.password
        form['anonymous'].value = "1" #Don't add me to the active users list
        browser.submit_form(form)

    def purchase(self, currency="ETH", plan="1m"):
        #Opens the page for the plans.
        websitevpnac = "https://airvpn.org/plans/"
        a = self.br.open(websitevpnac)
        self.br.session.headers['Referer'] = self.br.url

        #Finds the form for the plan.
        form = self.br.get_form(id="buy")
        form["plan"].value = plan
        self.br.submit_form(form)

        #Gets the redirection link
        b = str(self.br.find_all(class_="message_info"))
        explode = b.split('"')
        confirmation_page_link = "https://airvpn.org" + explode[3]
        confirmation_page_link = confirmation_page_link.replace("amp;", "")
        confirmation_page_link = confirmation_page_link.replace("§", "&sect")

        #Opens the link.
        self.br.open(confirmation_page_link)
        page = str(self.br.parsed)

        #Finds the login link and logs in
        login_link = str(self.br.get_link(text=re.compile("If you already have an account, click here to login"))).split('"')[1]
        login_link = login_link.replace("amp;", "")
        self.login(link=login_link)

        #Finds the page with the data-gateway for every currency.
        page = str(self.br.parsed)
        datagatewaylink = ""
        for line in page.split("\n"):
            if(line.find('new Ajax.Request( "https:') > -1):
                b = line.split('"')

                datagatewaylink = b[1] + "14" + b[3]


        #Opens a new browser and finds the data-gateway for the correcy currency
        temp_browser = RoboBrowser(parser='html.parser', history=True, user_agent=self.h)
        self.login(browser=temp_browser)
        temp_browser.open(datagatewaylink)
        dategateway_page = str(temp_browser.parsed)
        regex = 'data-currency="' + currency + '" data-gateway="(.+?)"'
        datagateway = re.findall(regex, dategateway_page)[0]

        #Uses the first browser to submit the form with the correct datagateway data
        page = self.br.parsed
        form = self.br.get_form(action="https://airvpn.org/index.php?app=nexus&module=payments&section=receive&do=validate")
        form['method_id'].value = "14"
        form.action = "/gateway_coinpayments?act=pay&data=" + datagateway
        self.br.submit_form(form)

        #Find the redirection link to the coinpayment website.
        page = self.br.parsed
        payment_link = str(self.br.get_link(text=re.compile("Or click here if"))).split('"')[1]
        payment_link = payment_link.replace("amp;", "")
        payment_link = payment_link.replace("¤", "&curren")
        print(payment_link)

        #Chooses the correct cryptocurrency and submits the form.
        self.br.open(payment_link)
        page = self.br.parsed
        form = self.br.get_form()
        form['checkout'].value = "1"
        form['selcoin'].value = currency
        self.br.submit_form(form)

        page = self.br.parsed
        print(page)


if __name__ == '__main__':
    a = airvpn()
    a.purchase()

