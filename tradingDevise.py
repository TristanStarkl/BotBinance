from binance.client import Client
from keys import *
from binance import ThreadedWebsocketManager
from time import sleep
from evaluate import *
import threading

clientBinance = Client(api_key, secret_key)

if ENVIRONNEMENT_TEST:
	client.API_URL = 'https://testnet.binance.vision/api'


# On définit la stratégie en cours, avec le prix moyen autorisé
#strategie = Strategie(375)
#print(client.get_asset_balance(asset="BTC"))
#btc_price = client.get_symbol_ticker(symbol="BNBBUSD")
#print(btc_price["price"])

# timePassed = 0
# while timePassed != 0:
# 	btc_price = client.get_symbol_ticker(symbol="BNBBUSD")
# 	btc_price = float(btc_price["price"])
# 	btcTradeHistory(btc_price)
# 	timePassed += 1
# 	sleep(1)
# print("VALUE DU COMPTE APRES X SECONDES: ", strategie.value(float(btc_price["price"])))

class tradingDevise(threading.Thread):
	def __init__(self, botName, client, deviseTraded, money2Started=50):
		threading.Thread.__init__(self)
		self.continuer = True
		self.client = client
		self.mutex = threading.Lock()
		self.deviseTraded = deviseTraded
		self.strategieUsed = "percentage"
		self.name = botName

	def trade(self):
		self.mutex.acquire()
		tokenPrice = self.client.get_symbol_ticker(symbol=self.deviseTraded)
		tokenPrice = float(tokenPrice["price"])
		if self.strategie is not None:
			actual_order = self.strategie.calculate(tokenPrice)
			if actual_order is not None:
				print("ORDER ", actual_order)
				self.client.create_order(
					symbol=actual_order["symbol"],
					side=actual_order["side"],
					type=actual_order["type"],
					quantity=actual_order["quantity"]
					)
		self.mutex.release()

	def initialize(self, initialPrice, strategieUsed="percentage"):
		if strategieUsed == "percentage":
			self.strategie = Strategie(self.client, initialPrice, self.deviseTraded)

	def value(self):
		return self.strategie.value()

	def run(self):
		while True:
			if self.continuer:
				self.trade()
				sleep(1)

	def release(self):
		self.continuer = False

	def restart(self):
		self.continuer = True

	def etat(self):
		if self.continuer:
			return "ALLUME"
		return "ETEINT"

"""
{'e': '24hrTicker', 'E': 1647039056366, 's': 'BTCUSDT', 'p': '-316.40000000', 'P': '-0.803', 'w': '39080.69214076', 'x': '39381.07000000',
 'c': '39064.68000000', 'Q': '0.00037000', 'b': '39064.68000000', 'B': '1.20923000', 'a': '39064.69000000', 'A': '1.39310000',
  'o': '39381.08000000', 'h': '40236.26000000', 'l': '38223.60000000', 'v': '59264.43224000', 'q': '2316095031.26840550', 'O': 1646952656298, 'C': 1647039056298, 'F': 1288474701, 'L': 1289730105, 'n': 1255405}
"""