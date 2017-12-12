from mechanize import Browser
from cloudomate.wallet import Wallet

class MullVad:
	accountnumber = "6798499523758101"
	website = "https://www.mullvad.net/account/login/"
	br = Browser()
	#wallet = Wallet()

	def __init__(self):
		self.br.set_handle_robots(False)
	
	#Login with given accountnumber
	def login(self):
		self.br.open(self.website)
		'''for form in br.forms():
			print "Form name:", form.name
			print form'''
		self.br.select_form(nr=0)
		self.br.form['account_number'] = self.accountnumber
		return self.br.submit()

	#Purchase 1 month VPN
	def purchase(self, account_page):
		self.br.open(account_page.geturl())
		'''for form in self.br.forms():
			print "Form name:", form.name
			print form'''
		self.br.select_form(nr=0)
		self.br.form['months'] = ['1',]
		purchase_page = self.br.submit()
		month_price = ""
		bitcoin_address = ""
		#Get the price for one month and bitcoin address from html code
		for line in purchase_page.read().split("\n"):
			if "1 month = " in line:
				month_price = line.strip().split(" ")[3]
			if 'input type="text"' in line:
				bitcoin_address = line.strip().split(" ")[2].split("=")[1]
		print(month_price)
		print(bitcoin_address)
		#return pay(bitcoin_address)

	#Pay for 1 month using bitcoins and the electrum wallet
	'''def pay(self, price, bitcoin_address):
		transaction_hash = self.wallet.pay(bitcoin_address, price)
		print(transaction_hash)
		if transaction_hash:
			return true
		else:
			return false'''

	#Setup the VPN
	def setupVPN():
		print("Time to setup the vpn!")
		#TODO: Setup VPN using openVPN and mullvad settings



if __name__ == '__main__':
	mv = MullVad()
	account_page = mv.login()
	#TODO: Add check if VPN is still valid before purchase
	#TODO: Add check if VPN is already installed
	if mv.purchase(account_page):
		mv.setupVPN()
	else:
		print("Transaction failed")
