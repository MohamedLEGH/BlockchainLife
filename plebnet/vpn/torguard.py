from robobrowser import RoboBrowser
import random
from plebnet.vpn import config
import sys

class torguard:
    headers = config.headers
    h = headers[random.randrange(len(headers))]
    br = RoboBrowser(parser='html.parser', history=True, user_agent=h)
    email = config.airvpn_username
    password = config.airvpn_password

    def __init__(self):
        print("This is the constructor")

    def login(self):
        websitelogin = "https://torguard.net/clientarea.php"
        self.br.open(websitelogin)
        page = str(self.br.parsed)
        print(page)

        #login fails because the website blocks robots
        form = self.br.get_form(action="https://torguard.net/dologin.php")
        print(form)
        form['username'].value = self.email
        form['password'].value = self.password
        self.br.submit_form(form)

    def purchase(self):
        print()



if __name__ == '__main__':
    t = torguard()
    t.login()

