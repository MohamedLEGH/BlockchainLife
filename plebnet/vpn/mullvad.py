from robobrowser import RoboBrowser
#from cloudomate.wallet import Wallet
import os

class MullVad:
	accountnumber = "6798499523758101"
	website = "https://www.mullvad.net/account/login/"
	br = RoboBrowser(parser='html.parser', history=True)
	#wallet = Wallet()
	
	#Login with given accountnumber
	def login(self):
		self.br.open(self.website)
		form = self.br.get_form()
		form['account_number'].value = self.accountnumber
		self.br.session.headers['Referer'] = self.website
		self.br.submit_form(form)

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
		#if pay(month_price, bitcoin_address):
		#	setupVPN()
		#else:
		#	print("Error: payment failed")

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
		#TODO: Setup VPN using openVPN and mullvad settings



if __name__ == '__main__':
	mv = MullVad()
	test_scraping = False
	test_payment = True
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
