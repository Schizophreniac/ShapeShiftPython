import requests
import json


def request(method, command):
	def request_decorator(request_func):
		def wrap_func(self, params=''):
			url = self.base_url + command + request_func(self, params)
			return self.do_request(url, method)
		return wrap_func
	return request_decorator


class ShapeShiftAPI:

	# https://info.shapeshift.io/api#api-3 - link to the ShapeShift API

	base_url = 'https://www.shapeshift.io/'

	def __init__(self):
		pass


	def do_request(self, url, method):
		if method == 'get':
			response = json.loads(requests.get(url).text)
			return response

		elif method == 'post':
			pass


	@request('get', 'rate/')
	def get_rate(self, params):
		"""
			Gets the current rate offered by Shapeshift. This is an estimate because the rate can
			occasionally change rapidly depending on the markets. The rate is also a 'use-able'
			rate not a direct market rate. Meaning multiplying your input coin amount times the
			rate should give you a close approximation of what will be sent out. This rate does
			not include the transaction (miner) fee taken off every transaction.
		"""
		return params['first_cur'] + '_' + params['second_cur']


	@request('get', 'limit/')
	def get_deposit_limit(self, params):
		"""
			Gets the current deposit limit set by Shapeshift. Amounts deposited over this limit
			will be sent to the return address if one was entered, otherwise the user will need
			to contact ShapeShift support to retrieve their coins. This is an estimate because a
			sudden market swing could move the limit.

		"""
		return params['first_cur'] + '_' + params['second_cur']

	@request('get', 'marketinfo/')
	def get_market_info(self, params):
		"""
			This gets the market info (pair, rate, limit, minimum limit, miner fee). 
		"""
		return params['first_cur'] + '_' + params['second_cur']


	@request('get', 'recenttx/')
	def get_recent_transaction_list(self, params):
		"""
			Get a list of the most recent transactions.
		"""
		return params['max']


	@request('get', 'getcoins/')
	def get_available_coins(self, params=''):
		"""
			Allows anyone to get a list of all the currencies that Shapeshift currently supports
			at any given time. The list will include the name, symbol, availability status, and
			an icon link for each.
		"""
		return params