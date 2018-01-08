from robobrowser import RoboBrowser
#from cloudomate.wallet import Wallet
import os
import zipfile
import shutil
import urllib.request
import sys

class MullVad:
	accountnumber = "6798499523758101"
	website = "https://www.mullvad.net/account/login/"
	br = RoboBrowser(parser='html.parser', history=True)
	#wallet = Wallet()

	#create account
	def createAccount(self):
		#Retrieve captcha for creating account and save it
		self.br.open("https://www.mullvad.net/en/account/create/")
		img = self.br.find("img", class_= "captcha")['src']
		urllib.request.urlretrieve("https://www.mullvad.net"+img,"captcha.png")
		#TODO: Use captcha solution for getting new accountnr and store that somewhere

	
	#Login with given accountnumber
	def login(self):
		self.br.open(self.website)
		form = self.br.get_form()
		form['account_number'].value = self.accountnumber
		self.br.session.headers['Referer'] = self.website
		self.br.submit_form(form)

	#checks if vpn expired, should be called after login
	def checkVPN(self):
		self.login()
		expire_date = self.br.select(".balance-header")[0].text
		expire_date = expire_date.split('\n')[2]
		temp1 = expire_date.index('in')
		temp2 = expire_date.index('days')
		expire_date = expire_date[temp1+3:temp2-1]
		#print(expire_date)
		if (expire_date <= '0'):
			print("Trying to puchase")
			self.purchase()

	#Purchase 1 month VPN
	def purchase(self):
		form = self.br.get_form()
		form['months'].value = "1"
		self.br.session.headers['Referer'] = self.br.url
		self.br.submit_form(form)
		month_price = ""
		bitcoin_address = ""
		payment_info_page = str(self.br.parsed)
		#Get the price for one month and bitcoin address from html code
		for line in payment_info_page.split("\n"):
			if "1 month = " in line:
				month_price = line.strip().split(" ")[3]
			if 'input readonly' in line:
				bitcoin_address_line = line.strip().split(" ")[3].split("=")[1]
				bitcoin_address = bitcoin_address_line.partition('"')[-1].rpartition('"')[0]
		print(month_price)
		print(bitcoin_address)
		if pay(month_price, bitcoin_address):
			self.setupVPN()
		else:
			print("Error: payment failed")

	#Pay for 1 month using bitcoins and the electrum wallet
	def pay(self, price, bitcoin_address):
		#Start electrum daemon
		os.system('electrum --testnet daemon start')
		#Load electrum default wallet
		os.system('electrum --testnet daemon load_wallet')
		#Check balance in wallet is enough for payment
		balance = os.popen('electrum --testnet getbalance').read()
		balance = float(balance.split("\n")[1].split(":")[1].replace('"', "").replace(" ", "").replace(",", ""))
		print(balance)
		if balance >= price:
			transaction = os.popen('electrum --testnet payto ' + bitcoin_address + ' ' + str(price) + '| electrum --testnet  broadcast -').read()
			#Check if transaction was successfull and return state of transaction
			transaction_complete = transaction.find('true')
			if transaction_complete == -1:
				transaction_complete = False
			else:
				transaction_complete = True
			print('transaction = ' + str(transaction_complete))
			return transaction_complete
		else:
			print('Insufficient balance, transaction cancelled')
			return False

	#Setup the VPN
	def setupVPN():
		print("Time to setup the vpn!")
		self.downloadFiles()
		#TODO: Setup VPN using openVPN and mullvad settings

	#Download config files for setting up VPN and extract them
	def downloadFiles(self):
		#Fill information on website to get right config files for openvpn 
		self.br.open("https://mullvad.net/en/download/config/")
		form = self.br.get_form()
		form['account_token'].value = self.accountnumber
		form['platform'].value = "Linux"
		form['region'].value = "se-sto"
		form['port'].value = "0"
		self.br.session.headers['Referer'] = self.br.url
		self.br.submit_form(form)
		content = self.br.response.content

		#Download the zip file to the right location
		files_path = "./installation-script/config.zip"
		with open(files_path, "wb") as output:
		  output.write(content)

		#Unzip files
		zip_file = zipfile.ZipFile(files_path, 'r')
		for member in zip_file.namelist():
			filename = os.path.basename(member)
			# skip directories
			if not filename:
				continue

		    # copy file (taken from zipfile's extract)
			source = zip_file.open(member)
			target = file(os.path.join("./installation-script/", filename), "wb")
			with source, target:
				shutil.copyfileobj(source, target)

		#Delete zip file
		os.remove(files_path)


if __name__ == '__main__':
	mv = MullVad()
	test_scraping = False
	test_payment = False
	test_downloading = False
	test_createAccount = False
	if test_scraping:
		mv.login()
		#TODO: Add check if VPN is still valid before purchase
		#TODO: Add check if VPN is already installed
		if mv.purchase():
			mv.setupVPN()
		else:
			print("Transaction failed")
	if test_payment:
		mv.pay(0.00027, "mfXuna4dtqrKW827BpWjzqkKDyqUjuzPz5")
	if test_downloading:
		mv.downloadFiles()
	if test_createAccount:
		mv.createAccount()
	#check if vpn is expired	
	if sys.argv[1] == "check":
		mv.checkVPN();
