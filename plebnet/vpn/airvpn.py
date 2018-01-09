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

    def login(self, link=None):
        if link is None:
            websitelogin = "https://airvpn.org/index.php?app=core&module=global&section=login"
        else:
            websitelogin = link

        print("link: " + str(link))
        self.br.open(websitelogin)
        page = str(self.br.parsed)

        form = self.br.get_form(action="https://airvpn.org/index.php?app=core&module=global&section=login&do=process")
        form['ips_username'].value = self.email
        form['ips_password'].value = self.password
        form['anonymous'].value = "1" #Don't add me to the active users list
        self.br.submit_form(form)

    def purchase(self):
        #self.login()
        websitevpnac = "https://airvpn.org/plans/"

        a = self.br.open(websitevpnac)
        self.br.session.headers['Referer'] = self.br.url

        #Finds the form for the plan.
        form = self.br.get_form(id="buy")
        form["plan"].value = "1m"
        self.br.submit_form(form)

        #https://airvpn.org/?app=nexus&module=payments&section=pay&id=701212

        #Gets the redirection link
        b = str(self.br.find_all(class_="message_info"))
        explode = b.split('"')
        link = "https://airvpn.org" + explode[3]
        link = link.replace("amp;", "")
        link = link.replace("§", "&sect")
        print("It goes to this link: " + link)

        self.br.open(link)
        page = str(self.br.parsed)
        #page = str(self.br.parsed)
        #print(page)

        login_link = str(self.br.get_link(text=re.compile("If you already have an account, click here to login"))).split('"')[1]

        print("Hier: " + login_link)

        login_link = login_link.replace("amp;", "")

        self.login(link=login_link)

        page = str(self.br.parsed)
        #print(page)

        self.br.get_form(action="https://airvpn.org/index.php?app=nexus&module=payments&section=receive&do=validate")
        print(form)

if __name__ == '__main__':
    a = airvpn()
    a.purchase()

