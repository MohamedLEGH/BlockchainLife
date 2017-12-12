import re
from cloudomate.gateway import bitpay
from mechanize import Browser
from bs4 import BeautifulSoup

#class ExpressVpn(self):

#       website_orderpage = "https://www.expressvpn.com/order"
#       required_settings = [
#               'email',
#               'password', 
#       ]
#       gateway = bitpay
#       price = column.find('div', {'class': 'order-total-value'}).text.strip()
#       br = self._create_browser()

#       def _create_browser():
#               br = Browser()
#               br.set_handle_robots(False)
#               br.addheaders = [('User-agent', random.choice(user_agents))]
#               return br

if __name__ == '__main__':
#       soup = BeautifulSoup("https://www.expressvpn.com/order", 'lxml')
        br = Browser()
        br.set_handle_robots(False)
        #br.addheaders = [('User-agent', random.choice(user_agents))]

        temp = br.open("https://www.expressvpn.com/order")
#       print(temp.read())
        soup = BeautifulSoup(temp.read(), 'html.parser')
        print(soup.prettify())
        for div in soup.findAll('div', {'name': 'signup[email]'}):
                print(div)


        for form in br.forms():
        #       print "Form name:", form.name
                print(form.name)
                for field in form._labels:
                        print(field)
                        print("\n********")
                        print(soup.findAll('div', {'name': 'signup[email]'}))
