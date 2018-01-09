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

    def login(self):
        websitelogin = "https://airvpn.org/index.php?app=core&module=global&section=login"
        self.br.open(websitelogin)
        page = str(self.br.parsed)

        form = self.br.get_form(action="https://airvpn.org/index.php?app=core&module=global&section=login&do=process")
        form['ips_username'].value = self.email
        form['ips_password'].value = self.password
        form['anonymous'].value = "1" #Don't add me to the active users list
        self.br.submit_form(form)

    def purchase(self):
        self.login()
        websitevpnac = "https://airvpn.org/plans/"
        self.br.session.headers['Referer'] = self.br.url
        a = self.br.open(websitevpnac)

        #Finds the form for the plan.
        form = self.br.get_form(id="buy")
        form["plan"].value = "1m"
        self.br.submit_form(form)

        #Gets the redirection link
        b = str(self.br.find_all(class_="message_info"))
        explode = b.split('"')
        link = "https://www.airvpn.org" + explode[3]
        print(link)
        #link = self.br.get_link(text=re.compile("here"))
        #self.br.follow_link(link)

        #Accessing the link result in a 404.
        self.br.open(link)
        page = str(self.br.parsed)
        print(page)



if __name__ == '__main__':
    a = airvpn()
    a.purchase()

