class GenerateShortenURLKey(object):
	""" class responsible for generating the url code """
	VALUES = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	BASE = 62
	
	def generate(self, number, code=""):
		if number > 0:
			code+=self.VALUES[int(number%self.BASE)]
			return self.generate(int(number/self.BASE), code)
		else:
			return code[::-1]
	

	def translate(self, code):
		number = 0
		list_code = list(code)
		for v in list_code:
			number *= self.BASE
			number += self.VALUES.index(v)
		return number