import mysql.connector

class MySqlConnection:

	def connect_mysql(self):
		return mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='url_shortening')

	def select_key(self):
		try:
			connector = self.connect_mysql()
			cursor = connector.cursor()
			query = (" UPDATE Seq_key SET id=LAST_INSERT_ID(id+1) ")
			cursor.execute(query)

			row = cursor.lastrowid
			
			self.key = row

			connector.commit()
			
		except Exception as e:

			return self.createDataError("ERROR TO GET NEW KEY", "", "005")

		finally:
			cursor.close()
			connector.close()

		return self.key

	def select_url_alias(self, alias):
		try:
			connector = self.connect_mysql()
			cursor = connector.cursor()

			query = (" SELECT full_url FROM url_Shortening where alias = %(alias)s ")
			cursor.execute(query, {'alias': alias})
			row = cursor.fetchone()
			if row:
				self.url = row[0]
			else:
				self.url = row
			
		except Exception as e:
			print(e)
			return self.createDataError("ERROR TO GET URL SHORTENING", alias, "004")
		finally:
			cursor.close()
			connector.close()

		return self.url


	def select_url(self, id):
		try:
			connector = self.connect_mysql()
			cursor = connector.cursor()
			query = (" SELECT full_url FROM Url_Shortening where id = %(id)s ")
			cursor.execute(query, {'id': id})
			row = cursor.fetchone()
			if row:
				self.url = row[0]
			else:
				self.url = row

		except Exception as e:
			print(e)
			return self.createDataError("ERROR TO GET URL SHORTENING", "", "004")

		finally:
			cursor.close()
			connector.close()

		return self.url

	def insert(self, data):
		try:
			connector = self.connect_mysql()
			cursor = connector.cursor()
			add_shorten_url = ("insert into url_shortening "
	               "(id, alias, url, full_url) "
	               "values (%(id)s, %(alias)s, %(url)s, %(full_url)s)")
			
			cursor.execute(add_shorten_url, data)
			
			# Make sure data is committed to the database
			connector.commit()

		except KeyError as error:	
			
			return self.createDataError("KEY ALREADY EXISTS", data['alias'], "002")

		except Exception as e:
			print(e)
			return self.createDataError("ERROR TO INSERT URL SHORTENING", data['alias'], "003")

		finally:
			cursor.close()
			connector.close()

		return data

	def createDataError(self, msg, alias, errorCode):
		error_data = {}
		error_data['alias'] = alias
		error_data['error_code'] = errorCode
		error_data['description'] = msg

		return error_data