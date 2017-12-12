from robobrowser import RoboBrowser
from cloudomate.wallet import Wallet

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
	mv.login()
	#TODO: Add check if VPN is still valid before purchase
	#TODO: Add check if VPN is already installed
	if mv.purchase():
		mv.setupVPN()
	else:
		print("Transaction failed")
