import json
import requests


def pair_to_str(pair):
	return '{f}_{s}'.format(s=pair.popitem()[1], f=pair.popitem()[1])


class ShapeShiftAPI:

	# https://info.shapeshift.io/api#api-3 - the ShapeShift API

	base_url = 'https://www.shapeshift.io/'

	def __init__(self):
		pass


	def do_request(self, url, method, data={}):
		if method == 'get':
			response = json.loads(requests.get(url).text)
			return response
		elif method == 'post':
			response = json.loads(requests.post(url, data=json.dumps(data)))
			return response


	# ------------------------
	#		Get requests 
	#  ----------------------- 
	def get_rate(self, pair):
		"""
			url: shapeshift.io/rate/[pair]
			method: GET
			 
			[pair] is any valid coin pair such as btc_ltc or ltc_btc
		"""
		command = 'rate/'
		method = 'get'
		url = self.base_url + command + pair_to_str(pair)
		return self.do_request(url, method)


	def get_deposit_limit(self, pair):
		"""
			url: shapeshift.io/limit/[pair]
			method: GET
			 
			[pair] is any valid coin pair such as btc_ltc or ltc_btc
		"""
		command = 'limit/'
		method = 'get'
		url = self.base_url + command + pair_to_str(pair)
		return self.do_request(url, method)


	def get_market_info(self, pair):
		"""
			url: shapeshift.io/marketinfo/[pair]
			method: GET
			 
			[pair] (OPTIONAL) is any valid coin pair such as btc_ltc or ltc_btc.
			The pair is not required and if not specified will return an array of all market infos.
		"""
		command = 'marketinfo/'
		method = 'get'
		url = self.base_url + command + pair_to_str(pair)
		return self.do_request(url, method)


	def get_recent_tx_list(self, number_of_tx=''):
		"""
			url: shapeshift.io/recenttx/[max]
			method: GET
			 
			[max] is an optional maximum number of transactions to return.
			If [max] is not specified this will return 5 transactions.
			Also, [max] must be a number between 1 and 50 (inclusive).
		"""
		if number_of_tx == '':
			command = 'recenttx/'
			method = 'get'
			url = self.base_url + command
			return self.do_request(url, method)
		else:
			try:
				if int(number_of_tx) >= 1 and int(number_of_tx) <= 50:
					command = 'recenttx/'
					method = 'get'
					url = self.base_url + command + str(number_of_tx)
					return self.do_request(url, method)
				else:
					return 'Number of transactions must be between 1 and 50.'
			except ValueError as err:
				print('ValueError: {e}.'.format(e=err))


	def get_deposit_status_to_address(self, addr):
		"""
			url: shapeshift.io/txStat/[address]
			method: GET
			 
			[address] is the deposit address to look up.
		"""
		command = 'txStat/'
		method = 'get'
		url = self.base_url + command + addr
		return self.do_request(url, method)


	def get_time_remaining_on_tx(self, addr):
		"""
			url: shapeshift.io/timeremaining/[address]
			method: GET
			 
			[address] is the deposit address to look up.
		"""
		command = 'timeremaining/'
		method = 'get'
		url = self.base_url + command + addr
		return self.do_request(url, method)


	def get_available_coins(self): 
		"""
			url: shapeshift.io/getcoins
			method: GET
		"""
		command = 'getcoins/'
		method = 'get'
		url = self.base_url + command
		return self.do_request(url, method)


	def get_tx_by_api_key(self, private_key):
		"""
			url: shapeshift.io/txbyapikey/[apiKey]
			method: GET
			 
			[apiKey] is the affiliate's PRIVATE api key.
		"""
		command = 'txbyapikey/'
		method = 'get'
		url = self.base_url + command + private_key
		return self.do_request(url, method)


	def get_tx_status_by_address(self, address, private_key):
		"""
			url: shapeshift.io/txbyaddress/[address]/[apiKey]
			method: GET
			 
			[address] the address that output coin was sent to for the shift
			[apiKey] is the affiliate's PRIVATE api key.
		"""
		command = 'txbyaddress/'
		method = 'get'
		url = self.base_url + command + address + '/' + private_key
		return self.do_request(url, method)


	def validate_tx(self, address, coin_symbol):
		"""
			url: shapeshift.io/validateAddress/[address]/[coinSymbol]
			method: GET
			 
			[address] the address that the user wishes to validate
			[coinSymbol] the currency symbol of the coin
		"""
		command = 'validateAddress/'
		method = 'get'
		url = self.base_url + command + address + '/' + coin_symbol
		return self.do_request(url, method)


	# --------------------------------
	#		Post requests
	# --------------------------------
	def do_normal_transaction(self, data={}):
		"""
			url:  shapeshift.io/shift
			method: POST
			data type: JSON
			data required:
			withdrawal     = the address for resulting coin to be sent to
			pair       = what coins are being exchanged in the form [input coin]_[output coin]  ie btc_ltc
			returnAddress  = (Optional) address to return deposit to if anything goes wrong with exchange
			destTag    = (Optional) Destination tag that you want appended to a Ripple payment to you
			rsAddress  = (Optional) For new NXT accounts to be funded, you supply this on NXT payment to you
			apiKey     = (Optional) Your affiliate PUBLIC KEY, for volume tracking, affiliate payments, split-shifts, etc...
			 
			example data: {"withdrawal":"AAAAAAAAAAAAA", "pair":"btc_ltc", returnAddress:"BBBBBBBBBBB"}
		"""
		url = 'https://www.shapeshift.io/shift'
		method = 'post'
		return self.do_request(url, method, data)


	def request_email_receipt(self, data={}):
		"""
			url:  shapeshift.io/mail
			method: POST
			data type: JSON
			data required:
			email    = the address for receipt email to be sent to
			txid     = the transaction id of the transaction TO the user (ie the txid for the withdrawal NOT the deposit)

			example data {"email":"mail@example.com", "txid":"123ABC"}
		"""
		url = 'https://www.shapeshift.io/mail'
		method = 'post'
		return self.do_request(url, method, data)


	def send_amount(self, data={}):
		"""
			url: shapeshift.io/sendamount
			method: POST
			data type: JSON
			 
			//1. Send amount request
			 Data required:
			amount          = the amount to be sent to the withdrawal address
			withdrawal      = the address for coin to be sent to
			pair            = what coins are being exchanged in the form [input coin]_[output coin]  ie ltc_btc
			returnAddress   = (Optional) address to return deposit to if anything goes wrong with exchange
			destTag         = (Optional) Destination tag that you want appended to a Ripple payment to you
			rsAddress       = (Optional) For new NXT accounts to be funded, supply this on NXT payment to you
			apiKey          = (Optional) Your affiliate PUBLIC KEY, for volume tracking, affiliate payments, split-shifts, etc...
			 
			example data {"amount":123, "withdrawal":"123ABC", "pair":"ltc_btc", returnAddress:"BBBBBBB"}

			//2. Quoted Price request
			//Note : This request will only return information about a quoted rate
			//       This request will NOT generate the deposit address.
			 
			Data required:
			amount  = the amount to be sent to the withdrawal address
			pair    = what coins are being exchanged in the form [input coin]_[output coin]  ie ltc_btc
			 
			example data {"amount":123, "pair":"ltc_btc"}

		"""
		url = 'https://www.shapeshift.io/sendamount'
		method = 'post'
		return self.do_request(url, method, data)


	def cancel_pending_tx(self, data={}):
		"""
			url: shapeshift.io/cancelpending
			method: POST
			data type: JSON
			data required: address  = The deposit address associated with the pending transaction
		"""
		url = 'https://www.shapeshift.io/cancelpending'
		method = 'post'
		return self.do_request(url, method, data)