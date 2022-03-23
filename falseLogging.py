import os


class logging():
	def __init__(self):
		self.level = "DEBUG"
		# Todo les différents systèmes de logs

	def log(self, message, tokenTraded):
		with open("./logs/{}.log".format(tokenTraded), "a+") as f:
			f.write(message)

	def initialize(self):
		if not os.path.exists("./logs/"):
			os.mkdir("./logs/")