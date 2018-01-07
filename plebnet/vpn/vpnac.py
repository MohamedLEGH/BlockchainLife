from robobrowser import RoboBrowser


class vpnac:
    br = RoboBrowser(parser='html.parser', history=True)
    links = []
    email = "chicker@tudelft.nl"
    password = "hoihoihoi"

    def hasnumbers(self, string):
        return any(char.isdigit() for char in string)

    def getpricesnew(self):
        websitevpnac = "https://www.vpn.ac/vpn-accounts"
        a = self.br.open(websitevpnac)
        page = str(self.br.parsed)

        price = self.br.find(name={"div"}, attrs={"class" : "box__price"})
        print(type(price))

        for i in price:
            print(str(i).strip())


    def getprices(self):
        websitevpnac = "https://www.vpn.ac/vpn-accounts"
        a = self.br.open(websitevpnac)
        page = str(self.br.parsed)

        # time/price found within these amount of lines
        timepricewithinlines = -1

        #1 for time, 2 for price
        timepriceidentifier = 0

        temp = ""
        result = ""

        for line in page.split("\n"):
            #If "timeframe" or "price" is found, then the time or price is found within 2 lines.
            if ("box__timeframe" in line):
                timepricewithinlines = 2
                timepriceidentifier = 1
            elif ("box__price" in line):
                timepricewithinlines = 2
                timepriceidentifier = 2

            if not(timepricewithinlines < 0):
                if self.hasnumbers(line):
                    temp = line
                    temp = temp.replace("<p>", "")
                    temp = temp.replace("</p>", "")
                    temp = temp.strip()

                    if (timepriceidentifier == 1):
                        result = temp + " - "
                    elif (timepriceidentifier == 2):
                        result = result + temp
                        print(result)
                        timepriceidentifier = 0 #reset to 0
                        timepricewithinlines = timepricewithinlines - 1

    def getpurchaselinks(self):
        websitevpnac = "https://www.vpn.ac/vpn-accounts"
        a = self.br.open(websitevpnac)
        page = str(self.br.parsed)
        linkNextLine = False

        for line in page.split("\n"):
            if(linkNextLine) :
                link = line.split("\"")[3]
                self.links.append(link)
                linkNextLine = False

            if("box__action" in line):
                linkNextLine = True

    def login(self):
        websitelogin = "https://www.vpn.ac/clientarea.php"
        self.br.open(websitelogin)

        form = self.br.get_form()
        form['username'].value = self.email
        form['password'].value = self.password
        self.br.submit_form(form)

        #newpage = self.br.parsed
        #print(str(newpage))

    def purchase(self):

        self.login()
        self.br.session.headers['Referer'] = self.br.url
        websitevpnac = "https://www.vpn.ac/cart.php?a=add&pid=1&billingcycle=monthly&promocode=DEC17&cc=1&skipconfig=1"
        a = self.br.open(websitevpnac)
        page = str(self.br.parsed)

        #Finds the checkout form.
        form = self.br.get_form(action='/cart.php?a=checkout')
        forms = self.br.get_forms()
        print(form.parsed)

        #Registration input
        #form['country'].value = 'Netherlands'
        #form['email'].value = self.email
        #form['password'].value = self.password
        #form['password2'].value = self.password

        #form['notes'].value = "Hello... It's me"
        form['paymentmethod'].value = 'coinpayments'

        self.br.submit_form(form)

        print('\n\n\n\n\n newpage \n')

        newpage = str(self.br.parsed)
        print(newpage)

        coinform = self.br.get_forms()
        self.br.submit_form(coinform[1])

        print('\n\n\n\n\n newpageaftercoin \n')

        newpage = str(self.br.parsed)
        print(newpage)
        print('\n\n\n\n')
        coinpaymentsform = self.br.get_form()
        coinpaymentsforms = self.br.get_forms()
        print('forms length:' + str(len(coinpaymentsforms)))
        coinpaymentsform['selcoin'].value = 'ETH'
        coinpaymentsform['first_name'].value = 'private'
        coinpaymentsform['last_name'].value = 'user'
        coinpaymentsform['checkout'].value = '1'
        coinpaymentsform['email'].value = self.email
        print(coinpaymentsform)

        self.br.submit_form(coinpaymentsform)

        print('\n\n\n\n\n lastpage \n')
        lastpage = str(self.br.parsed)
        print(lastpage)

    def test(self):
        website = "http://www.ka-wing.nl/scrape"
        a = self.br.open(website)
        page = str(self.br.parsed)
        form = self.br.get_forms();
        field = self.br

        all = self.br.find_all({'input' : True})

        print("\n\n\n")

        print(all)



if __name__ == '__main__':
    v = vpnac()
    v.purchase()
