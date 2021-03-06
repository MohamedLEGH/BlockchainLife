import time
import re
import sys
from selenium import webdriver
import requests
import os

class vpnac:
    COINPAYMENTS_URL = "https://www.coinpayments.net/index.php?cmd=checkout"
    PURCHASE_URL = "https://vpn.ac/vpn-accounts"

    # Use this method for purchasing with Bitcoin.
    def retrieve_bitcoin(self, user_settings):
        try:
            return self._retrieve_payment_info(["bitcoin", "BTC"], user_settings)
        except Exception as e:
            print(self._error_message(e))

    # Use this method for purchasing with Litecoin.
    def retrieve_litecoin(self, user_settings):
        try:
            return self._retrieve_payment_info(["litecoin", "LTC"], user_settings)
        except Exception as e:
            print(self._error_message(e))

    # Use this method for purchasing with Ethereum.
    # Retrieving Ethereum at the final page is different than for the other currencies.
    def retrieve_ethereum(self, user_settings):
        try:
            return self._retrieve_payment_info(["ethereum", "ETH"], user_settings)
        except Exception as e:
            print(self._error_message(e))

    # Used for generating error message.
    def _error_message(self, message):
        return "Error " + str(message) + "Try again. It it still does not work, " \
                                         "website might have been updated, update script."

    # Don't invoke this method directly.
    def _retrieve_payment_info(self, currency, user_settings):

        res = requests.get('https://chromedriver.storage.googleapis.com/2.35/chromedriver_linux64.zip')
        file_test = os.path.dirname(os.path.realpath(__file__)) + '/chromedriver_linux64.zip'
        with open(file_test, 'wb') as output:
            output.write(res.content)
            pass
        unzip_command = 'unzip -o ' + file_test + ' -d ' + os.path.dirname(os.path.realpath(__file__)) + '/'
        test_ = os.popen(unzip_command).read()
        os.popen('rm ' + file_test).read()
        print(test_)
        driver_loc = os.path.dirname(os.path.realpath(__file__)) + '/chromedriver'
        print("driver location: " + driver_loc)

        # Selenium setup: headless Chrome, Window size needs to be big enough, otherwise elements will not be found.
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('disable-gpu');
        options.add_argument('window-size=1920,1080');
        driver = webdriver.Chrome(executable_path=driver_loc,chrome_options=options)
        driver.maximize_window()

        print("Placing an order.")

        driver.get(self.PURCHASE_URL)
        driver.find_element_by_xpath('//*[@id="content"]/main/article[1]/div/div[1]/div[1]/div/div[3]/a').click()
        time.sleep(1)

        if user_settings.get("registered") == "1":
            driver.find_element_by_xpath('//*[@id="existingcust"]').click()
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="loginfrm"]/table/tbody/tr[1]/td[2]/input').\
                send_keys(user_settings.get("email"))
            driver.find_element_by_xpath('//*[@id="loginfrm"]/table/tbody/tr[2]/td[2]/input').\
                send_keys(user_settings.get("password"))
            driver.find_element_by_xpath('//*[@id="pgbtncoinpayments"]').click()
            time.sleep(1)
        else:
            driver.find_element_by_xpath('//*[@id="signupfrm"]/table/tbody/tr[3]/td[2]/input').\
                send_keys(user_settings.get("email"))
            driver.find_element_by_xpath('//*[@id="newpw"]').send_keys(user_settings.get("password"))
            driver.find_element_by_xpath('//*[@id="signupfrm"]/table/tbody/tr[5]/td[2]/input').\
                send_keys(user_settings.get("password"))

        driver.find_element_by_xpath('//*[@id="whmcsorderfrm"]/div[4]/input').click()

        time.sleep(2)

        print("Retrieving the amount and address.")

        if(user_settings.get("registration") == "0"):
            pass # Change registration to 1 for ever.

        driver.find_element_by_xpath('//*[@id="cpsform"]/input[15]').click()
        time.sleep(1)
        driver.find_element_by_id("coins_" + currency[1]).click()
        time.sleep(1)
        driver.find_element_by_id("dbtnCheckout").click()
        time.sleep(1)

        tries = 0
        while not (driver.current_url == self.COINPAYMENTS_URL):
            tries = tries + 1
            time.sleep(2)
            if tries > 10:
                raise Exception("You probably already have 3 unfinished transfers with coinpayments.net from within "
                                "the last 24 hours and you therefore cannot create anymore.")

        amount = ""
        address = ""

        page = driver.page_source
        address_re = ""
        amount_re = ""
        if currency[0] == "ethereum":
            address_re = '<div class="address">(.*?)</div>'
            amount_re = "<div>(.*?) ETH</div>"
        else:
            address_re = '<div><a href="' + currency[0] + ':(.*?)\?amount=(.*?)">(.*?)</a></div>'

        # Get address and amount
        if currency[0] == "ethereum":
            for line in page.split('\n'):
                line = line.lstrip().rstrip()
                match_amount = re.findall(amount_re, line)
                match_address = re.findall(address_re, line)
                if len(match_amount) > 0:
                    amount = match_amount[0]
                if len(match_address) > 0:
                    address = match_address[0]
        else:
            for line in page.split('\n'):
                line = line.lstrip().rstrip()
                match = re.findall(address_re, line)
                if len(match) > 0:
                    address = match[0][0]
                    amount = match[0][1]

        time.sleep(2)
        return {'amount': str(amount), 'address': str(address)}
    def pay(self,bitcoinadress,amount):
        #pay the amount to the address with the scpefified currency (if enough balance), otherwise print message "Bticoin/Ethereum Balance not enough" (depending on the currency chosen)
        print("\nconnect")
        pass
if __name__ == "__main__":
    user_settings = {"email": "ralphie_obswest@hotmail.com", "password": "Chicker", "registered": "1"}

    a = vpnac()
    b = a.retrieve_bitcoin(user_settings)
    print(b['amount'])
    print(b['address'])
    time.sleep(200)
    a.pay(b['address'],b['amount'])
    time.sleep(200)
