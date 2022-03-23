from numpy import random
import math
from falseLogging import logging

logs = logging()
logs.initialize()

ACHAT = True
VENTE = False

class order():
	def __init__(self, typeOrder, price, quantityBought):
		self.typeOrder = typeOrder
		self.price = price
		self.quantityBought = quantityBought

	def __repr__(self):
		verbe = "Acheté" if self.typeOrder == ACHAT else "Vendu"
		return "On a {} ({} BTC pour un total de {}, prix unitaire {})".format(verbe, str(self.quantityBought), str(self.quantityBought * self.price), str(self.price))



def round_decimals_down(number:float, decimals:int=5):
    """
    Returns a value rounded down to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more")
    elif decimals == 0:
        return math.floor(number)

    factor = 10 ** decimals
    return math.floor(number * factor) / factor

class Strategie():
	def __init__(self, client, firstBuyMaxPrice, token):
		self.position = ACHAT
		self.lastPrice = 0
		self.allTrades = []
		self.profits = 0
		self.lastBuyPrice = 0
		self.lastSellPrice = firstBuyMaxPrice
		self.quantityUSDT = 50
		self.quantityBought = 0
		self.stopLossCurrentStreak = 0
		self.savedUSDT = 0
		self.token = token
		infos = client.get_symbol_info(token)
		self.minQty = float(infos["filters"][2]["minQty"])
		self.lotSize = float(infos["filters"][2]["stepSize"])
		string = "L'achat initial {} sera fait à {}".format(self.token, str(0.98 * firstBuyMaxPrice))
		self.log(string)

	def log(self, message):
		logs.log(message + "\n", self.token)
		print("{}: ".format(self.token), message)

	def calculate(self, newPrice):
		self.lastPrice = newPrice
		if newPrice <= 0.85 * self.lastBuyPrice:
			self.stopLossCurrentStreak += 1
			if self.stopLossCurrentStreak > 20:
				self.log("ON PANIC SELL A : {}".format(str(newPrice)))
				# On vend pour Limiter les pertes
				wonUSDT = self.quantityBought * newPrice
				saved = 0
				if (wonUSDT > 50):
					saved = round((wonUSDT - 50) / 2, 2)
				self.savedUSDT += saved
				self.position = ACHAT
				quantitySelled = self.quantityBought
				self.lastSellPrice = newPrice
				self.allTrades.append(order(VENTE, newPrice, quantitySelled))
				self.quantityBought = 0
				self.stopLossCurrentStreak = 0
				return {"symbol":self.token, "side":"SELL", "type":"MARKET","quantity":quantitySelled}


		if self.position == ACHAT:
			if newPrice <= 0.995 * self.lastSellPrice:
				quantity = self.quantityUSDT / newPrice
				quantity2 = quantity // self.lotSize
				quantity = quantity2 * self.lotSize
				quantity = round_decimals_down(quantity)
				newOrder = order(ACHAT, newPrice, quantity)
				if (quantity < self.minQty):
					self.log("La quantité est inférieure à la quantité minimum")
					return None
				self.quantityBought = quantity
				self.position = VENTE
				self.lastBuyPrice = newPrice
				self.allTrades.append(newOrder)
				self.stopLossCurrentStreak = 0
				self.quantityUSDT = 0
				dictionnary = {"symbol":self.token, "side":"BUY", "type":"MARKET","quantity":self.quantityBought, "PRICE": newPrice}
				self.log(str(dictionnary))
				return dictionnary
			else:
				pass
		elif self.position == VENTE:
			if newPrice >= 1.005 * self.lastBuyPrice:
				wonUSDT = self.quantityBought * newPrice
				quantitySelled = self.quantityBought
				saved = 0
				if (wonUSDT > 50):
					saved = round((wonUSDT - 50) / 2, 2)
				self.quantityUSDT = wonUSDT - saved
				self.savedUSDT += saved
				self.position = ACHAT
				self.lastSellPrice = newPrice
				self.allTrades.append(order(VENTE, newPrice, quantitySelled))
				self.quantityBought = 0	
				self.stopLossCurrentStreak = 0
				dictionnary = {"symbol":self.token, "side":"SELL", "type":"MARKET","quantity":quantitySelled, "PRICE": newPrice}
				return dictionnary
		return None

	def __repr__(self):
		string = ""
		for orders in self.allTrades:
			string += orders.__repr__()
			string += "\n"
		return "La liste de nos positions est de \n" + string

	def value(self):
		price = self.lastPrice
		assetsValue = self.quantityBought * price
		assetsValue += self.quantityUSDT
		assetsValue += self.savedUSDT
		dev = {
			"TokenBought": self.quantityBought,
			"TokenPrice": price,
			"USDT": self.quantityUSDT,
			"SAVED" : self.savedUSDT
		}
		return (assetsValue, dev)


def evaluateRentability():
	averageRentability = []
	averageSaved = []
	for i in range(400):
		bot = Strategie(37500, "BTCUSDT")
		jeuTest = random.normal(37500, 2500, 50)

		for price in jeuTest:
			bot.calculate(price)
		averageRentability.append(bot.value(42000)[0])
		averageSaved.append(bot.value(0)[1]["SAVED"])
	mean = sum(averageRentability) / len(averageRentability)
	meanS = sum(averageSaved) / len(averageSaved)
	maxR = max(averageRentability)
	minR = min(averageRentability)
	print("En moyenne on a {}$ (x{} de la mise de départ) , soit une augmentation de {}%. Les meilleures performances sont {}$ ({}%) et la pire est {}$ ({}%). La quantité moyenne sauvée est de {}".format(
		str(round(mean, 2)), str(round(mean / 50, 2)), str(round(((round(mean, 2) * 100)/ 50) - 100, 2)), str(round(maxR, 2)), str(round((maxR * 100 / 50) - 100, 2)), str(round(minR, 2)), str(round((minR * 100 / 50) - 100, 2))
		, str(round(meanS, 2))
		))

if __name__ == "__main__":
	#bot = Strategie(37500)
	#for price in jeuTest:
	#	bot.calculate(price)
	#print(bot)
	#print(bot.value(37500))
	evaluateRentability()