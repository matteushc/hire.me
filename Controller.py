from MySqlConnection import MySqlConnection
from GenerateShortenURLKey import GenerateShortenURLKey
import time

class Controller(object):
	"""docstring for Controller"""
	BASE_URL = "http://shortener/u/"

	def __init__(self):
		self.mysql = MySqlConnection()
		self.shorten = GenerateShortenURLKey()


	def createWithAlias(self, url, alias):
		start_time = time.time()

		self.url = self.mysql.select_url_alias(alias)
		print("url -> " + str(self.url))
		print("alias -> " + str(alias))
		if self.url:
			return self.mysql.createDataError("CUSTOM ALIAS ALREADY EXISTS", alias, "001")
		else:
			self.key = self.mysql.select_key()
			print("key ->" + str(self.key))	
			data = self.createData(self.key, alias, url)
			print("data - >" + str(data))
			final_data = self.mysql.insert(data)
			final_data['statistics'] = self.createStatis(start_time)
			return final_data
		

	
	def createWithoutAlias(self, url):
		start_time = time.time()
		self.key = self.mysql.select_key()
		self.alias = self.shorten.generate(self.key)
		
		data = self.createData(self.key, self.alias, url)
		final_data = self.mysql.insert(data)
		final_data['statistics'] = self.createStatis(start_time)
		return final_data


	def retrieveUrl(self, url):
		alias = url.rsplit('/', 1)[-1]
		self.key = self.shorten.translate(alias)
		self.url = self.mysql.select_url(self.key)
		if self.url:
			print("Recuperou pela url")
			return self.url
		else:
			print("Recuperou pelo alias")
			return self.mysql.select_url_alias(alias)	


	def createData(self, id, alias, full_url):
		self.BASE_URL += alias
		data = {}
		data['id'] = id
		data['alias'] = alias
		data['url'] = self.BASE_URL
		data['full_url'] = full_url
		return data

	def createStatis(self, start_time):
		final_time = time.time() - start_time
		statis = { "time_taken": str(final_time) + "ms"}		
		return statis