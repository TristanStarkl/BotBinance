from binance.client import Client
from keys import *
from binance import ThreadedWebsocketManager
from time import sleep
from strategie import *
import threading
from tradingDevise import tradingDevise

clientBinance = Client(api_key, secret_key)

if ENVIRONNEMENT_TEST:
	client.API_URL = 'https://testnet.binance.vision/api'

# On définit la stratégie en cours, avec le prix moyen autorisé
#strategie = Strategie(375)
#print(client.get_asset_balance(asset="BTC"))
#btc_price = client.get_symbol_ticker(symbol="BNBBUSD")
#print(btc_price["price"])

def btcTradeHistory(actualPrice):
	actualPrice = float(actualPrice)
	actualOrder = strategie.calculate(actualPrice)
	if actualOrder is not None:
		#market_order = client.create_test_order(actualOrder)
		print("ORDER: ", actualOrder)


# timePassed = 0
# while timePassed != 0:
# 	btc_price = client.get_symbol_ticker(symbol="BNBBUSD")
# 	btc_price = float(btc_price["price"])
# 	btcTradeHistory(btc_price)
# 	timePassed += 1
# 	sleep(1)
# print("VALUE DU COMPTE APRES X SECONDES: ", strategie.value(float(btc_price["price"])))

class tradingBot():
	def __init__(self):
		self.listDevisesTraded = []
		self.binanceClient = Client(api_key, secret_key)

	def addANewDevise(self, botName, deviseTraded, initialPrice, startingToken=50, strategieUsed="percentage"):
		devise = tradingDevise(botName, self.binanceClient, deviseTraded, startingToken)
		print(initialPrice)
		devise.initialize(float(initialPrice), strategieUsed)
		devise.start()
		self.listDevisesTraded.append(devise)

	def getEtatDevise(self, botName):
		data = "Le nom cherché n'est pas trouvé."
		for devises in self.listDevisesTraded:
			if devises.name == botName:
				devises.mutex.acquire()
				data = devises.value()
				devises.mutex.release()
				break
		return data

	def getListDevises(self):
		data = "Liste des trades actifs:\n"
		for name in self.listDevisesTraded:
			data += name.name 
			data += "\n"
		return data

	def getPriceForDevise(self, deviseName):
		tokenPrice = self.binanceClient.get_symbol_ticker(symbol=deviseName)
		data = "La devise {} s'échange actuellement à {}".format(deviseName, tokenPrice["price"])
		return data

"""
{'e': '24hrTicker', 'E': 1647039056366, 's': 'BTCUSDT', 'p': '-316.40000000', 'P': '-0.803', 'w': '39080.69214076', 'x': '39381.07000000',
 'c': '39064.68000000', 'Q': '0.00037000', 'b': '39064.68000000', 'B': '1.20923000', 'a': '39064.69000000', 'A': '1.39310000',
  'o': '39381.08000000', 'h': '40236.26000000', 'l': '38223.60000000', 'v': '59264.43224000', 'q': '2316095031.26840550', 'O': 1646952656298, 'C': 1647039056298, 'F': 1288474701, 'L': 1289730105, 'n': 1255405}
"""