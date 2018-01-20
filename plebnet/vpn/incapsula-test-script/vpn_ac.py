from vpn_hoster import VpnHoster
from vpn_hoster import VpnStatus
from vpn_hoster import VpnInfo
import requests
import sys
from time import sleep
from incapsula import IncapSession, RecaptchaBlocked
from reCaptchaSolver import reCaptchaSolver

class AcVpn(VpnHoster):

    PAYMENT_URL = 'https://www.vpn.ac/cart.php?a=add&pid=1&billingcycle=monthly&promocode=DEC17&cc=1&skipconfig=1'
    LOGIN_URL = 'https://www.vpn.ac/clientarea.php'

    TEMP_URL = 'https://www.coinpayments.net/index.php?cmd=checkout'


    username = 'chicker4@tudelft.nl'
    password = 'hoihoihoi'

    def __init__(self):
        super().__init__()

        self.name = "vpnac"
        self.website = "https://vpn.ac"
        self.protocol = "OpenVPN"
        self.bandwidth = sys.maxsize
        self.speed = sys.maxsize

    def login(self):
        self.br.open(self.LOGIN_URL)
        form = self.br.select_form()
        #print(form.print_summary())

        form["username"] = self.username
        form["password"] = self.password


        #print("\n\n------------------------\n\n")

        #print(form.print_summary())

        #print(self.br.get_current_page())
        page = self.br.submit_selected()

        if page.url == self.LOGIN_URL: #TODO check div id account-snapshot exists -> if so -> login successfull
            pass
        return page

    def purchase(self):
        self.br.open(self.PAYMENT_URL)
        form = self.br.select_form('#mainfrm')
        form["paymentmethod"] = "coinpayments"
        self.br.submit_selected()

        print("\n\n***************************************\n\n")
        #print(self.br.get_current_page())

        self.br.select_form('#cpsform')
        self.br.submit_selected()
        #print(self.br.get_current_page())

        form = self.br.select_form('#coform')
        form['selcoin'] = 'ETH'
        form['first_name'] = 'private'
        form['last_name'] = 'user'
        form['checkout'] = '1'
        form['email'] = self.username
      #  print(form.print_summary())
       # print("\n######\n")
        print((self.br.session.cookies))

       # print((self.br.session.cookies.add_cookie_header(self.br.session)))

        cookielist = []

        inc_session = IncapSession(1000)

        for cookie in self.br.session.cookies.items():
            if(cookie[0] == 'PHPSESSID'):
                print("*** -->cookie: ")
                cookielist.append("=".join(cookie))
                inc_session.cookies.set(cookie[0], cookie[1])
                print(cookielist)
            elif 'visid_incap' in cookie[0]:
                print("*** -->cookie: ")
                cookielist.append("=".join(cookie))
                inc_session.cookies.set(cookie[0], cookie[1])
                print(cookielist)
            elif 'incap_ses' in cookie[0]:
                print("*** -->cookie: ")
                cookielist.append("=".join(cookie))
                inc_session.cookies.set(cookie[0], cookie[1])
                print(cookielist)

        temp_cookie = "; ".join(cookielist)
        print("-----" + temp_cookie)

         #   temp = "=".join(cookie)
         #   cookielist.append(temp)
           # print("=".join(cookie))
           # print(cookie[1])

      #  print("------- csrf")
     #   print(form['csrf'])
     #   cookielist = ";".join(cookielist)
       # cookielist.replace("\n", "")
        print("\n###### Cookie HEADER \n")
    #    print(cookielist)
        #self.br.session.headers.update({'Cookie':'PHPSESSID=b4s66e8vt750qum87fs5hi60m2shp0bt; visid_incap_992349=9TVEVef5Qa22SZWbkE49HcGeU1oAAAAAQUIPAAAAAAAmh7e0y0CGHpccuwaablnK; incap_ses_451_992349=/bjPWgGG3CirFTGY60ZCBrfNVFoAAAAAIFqXttNnV1AGRv3AUWMFVA==; incap_ses_767_992349=sfruQXcovEcuHpZDl+6kCmO9VFoAAAAAy4MIsBAx2I27HQLvbdIqug=='})



        self.br.session.headers.update({'Cookie':temp_cookie})
        print("\n######\n")
        print((self.br.session.headers))

        print("\n######\n")
        #form['csrf'] = '33ccd51fb327a6412cc7a104ee23f8a78713ce5cfb19f4877c235826ec8c27de'
        #print(form.print_summary())
        print("\n######\n")
        self.br.submit_selected()
        print(self.br.get_current_page())

        print('Sleeping 5 sec .....')
        sleep(5)

        print("\n\n\n--------------------------------------------------\n\n")

        self.br.session.headers.update({'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})
        self.br.session.headers.update({'Connection': 'keep-alive'})
        self.br.session.headers.update({'Accept-Encoding': 'gzip, deflate, br'})
        self.br.session.headers.update({'Upgrade-Insecure-Requests': '1'})
        self.br.session.headers.update({'Accept-Language': 'en-US,en;q=0.5'})
        self.br.session.headers.update({'DNT': '1'})
        self.br.session.headers.update({'Host': 'www.coinpayments.net'})
        self.br.session.headers.update({'Cookie': temp_cookie})

        inc_session.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        inc_session.headers['Connection'] = 'keep-alive'
        inc_session.headers['Accept-Encoding'] = 'gzip, deflate, br'
        inc_session.headers['Upgrade-Insecure-Requests'] = '1'
        inc_session.headers['Accept-Language'] = 'en-US,en;q=0.5'
        inc_session.headers['DNT'] = '1'
        inc_session.headers['Host'] = 'www.coinpayments.net'
        inc_session.headers['Cookie'] = temp_cookie
        inc_session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0'


        #response = self.br.open(self.TEMP_URL)

      #  print(response.text)
       # print(response.headers)
       # if 'gaIframe' in response.text:
       #     print("\n\n____________&_____________\n\n")
       #     tempresponse = self.br.open('https://content.incapsula.com/jsTest.html')
       #     print(tempresponse.text)
       #     pass

       # print("\n\n________------------------____\n\n")
       # print(self.br.get_current_page())
        #headersprev = self.br.session.headers

        #print(inc_session.headers)


        try:
            response = inc_session.get(self.TEMP_URL)
        except RecaptchaBlocked as e:
            print("\n\n\n\----------------------Recaptcha----------------------------\n\n")
            print(e.response)
            print(e.response.text)
            print("\n\n\n\----------------------Recaptcha URL----------------------------\n\n")
            print(e.response.url)
            print("\n\n\n\----------------------Select Recaptcha----------------------------\n\n")
            rc_solver = reCaptchaSolver("fd58e13e22604e820052b44611d61d6c")
            elem_s = ""
            for item in e.response.text.split("\n"):
                if 'data-sitekey="' in item:
                    elem_s = item.split('data-sitekey="', 1)[-1]
                    re_captcha_site_key = elem_s.split('"')[0]
                    print("\n\n\n\n\n\n---------Site KEy---------\n\n\n\n\n")
                    print(re_captcha_site_key)
                    for item2 in e.response.text.split("\n"):
                        if 'xhr.open("POST", "/_Incapsula_Resource?' in item2:
                            elem_s2 = item2.split('xhr.open("POST", "',1)[-1]
                            post_recaptcha_url = elem_s2.split('", true);')[0]
                            print("\n\n\n-----url ---->")
                            post_recaptcha_url = 'https://www.coinpayments.net' + post_recaptcha_url
                            print(post_recaptcha_url)

                            wUrl = e.response.url
                            wKey = re_captcha_site_key
                            rc_solution = rc_solver.solveGoogleReCaptcha(wUrl, wKey)
                            print("\n\nCaptcha solution -------->>" + rc_solution + "\n\n\n")
                            r_temp = requests.post(post_recaptcha_url, headers = {'Content-Type': 'application/x-www-form-urlencoded'}, data = {'g-recaptcha-response':rc_solution})
                            print("\n\n\n\n\n\n\n--------------------------------------------------------->>>>>>>\n\n\n\n\n")
                            print(r_temp)
                            print(r_temp.text)
                            print(r_temp.headers)
                            r_t_h_c = r_temp.headers['Set-Cookie']
                            print("\n\n\n\n\-->" + r_t_h_c +"\n\n")

                            #x_temp = requests.get(post_recaptcha_url)
                            #print("\n\n\n\n\n::::::\n\n\n\n\n\n\n")
                            #print(x_temp)
                            #print(x_temp.text)
                            self.br.session.headers.update({'Cookie': r_t_h_c})
                            self.br.open(post_recaptcha_url)
                            print(self.br.get_current_page())

                            self.br.open(self.TEMP_URL)
                            print(self.br.get_current_page())
                           # print(r_temp)
                            #print(r_temp.text)
                            #requests.open(r_temp.url)


                            #response = inc_session.get(self.TEMP_URL)
                            #print(response.text)
                            #r_t = requests.open(response.url)
                            #print(r_t.text)

                            break
                    break
            #print(e.response.select('div.g-recaptcha'))
            #rc_solver = reCaptchaSolver("fd58e13e22604e820052b44611d61d6c")
            #temp = rc_solver.getBalance()
            #print("test: " + str(temp))
            #print("___________________________________________________________________________")
            #wUrl = "http://http.myjino.ru/recaptcha/test-get.php"
            #wKey = "6Lc_aCMTAAAAABx7u2W0WPXnVbI_v6ZdbM6rYf16"
            #rc_solution = rc_solver.solveGoogleReCaptcha(wUrl, wKey)
            #print("\n\n******* hash solution: ****** \n\n" + rc_solution + "\n\n*******\n\n")
          #  tempresponse = self.br.open(self.TEMP_URL)
          #  print(self.br.get_current_page)
      #      if 'gaIframe' in tempresponse.text:
       #         print("\n\n____________&_____________\n\n")
     ##           tempresponse = self.br.open('https://content.incapsula.com/jsTest.html')
    #            print(tempresponse.text)
     #           pass
      #      else:
     #  #         print("\n\n***** *******\n\n")
      #          print("\n\n***** *******\n\n")
       #         print("\n\n***** *******\n\n")
       #         print("\n\n***** *******\n\n")
       #         print("\n\n***** *******\n\n")
        #        print(tempresponse.text)
      #      print("\n\n***** *******\n\n")
      #      print(e.response)

         #Handling re-captcha blocks.
#        try:
 #           print("\n\n\n--------------------------------------------------\n\n")
  #          #response = inc_session.get(self.TEMP_URL,True,headers=headersprev)
   #         response = inc_session.get(self.TEMP_URL,True)
    #    except RecaptchaBlocked as e:
     #       print("\n\n\n\----------------------Recaptcha----------------------------\n\n")
#            tempresponse = self.br.open(self.TEMP_URL)
 #           if 'gaIframe' in tempresponse.text:
  #              print("\n\n____________&_____________\n\n")
   #             tempresponse = self.br.open('https://content.incapsula.com/jsTest.html')
    #            print(tempresponse.text)
     #           pass
#
 #           print(inc_session.response)
  #          print("\n\n***** *******\n\n")
   #         print(e.response)
    #        raise

       # self.br.open(self.TEMP_URL)
        #print(self.br.get_current_page())


        #response = inc_session.get(self.TEMP_URL, headers=headersprev)
      #  print(response.text)


       # print("\nSleeping 5 sec.....\n")
        #sleep(5)
        #self.br.open(self.TEMP_URL)
       # print(self.br.get_current_page())
       # print(self.br.session.headers)




if __name__ == '__main__':
    vpnac = AcVpn()
    vpnac.login()
    vpnac.purchase()