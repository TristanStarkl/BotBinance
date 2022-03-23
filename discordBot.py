import discord
import asyncio
import time
from random import randint, choice, SystemRandom
import logging
import re
import os
from tradingBot import tradingBot
from keys import *

Client = discord.Client(command_prefix="")
bot = tradingBot()

@Client.event
async def on_message(message):
	if (Client.user.id == message.author.id):
		return
	if (message.content.startswith(".start bot")):
		await message.channel.send("Lancement du bot effectué.")

	if (message.content.startswith(".create trade")):
		categories = message.content.split(" ")
		if (len(categories) == 5):
			botName = categories[2]
			devise = categories[3]
			starting_price = categories[4]
			bot.addANewDevise(botName, devise, starting_price)
			await message.channel.send("Création du trade automatique créé.")
		else:
			await message.channel.send("Usage: .create trade botName devise startingPrice")

	if (message.content.startswith(".switch bot off")):
		bot.release()
		await message.channel.send("Arrêt du bot en cours.")

	if (message.content.startswith(".bot etat")):
		message2 = "Etat du bot: "
		message2 += bot.etat()
		await message.channel.send(message2)

	if (message.content.startswith(".get devise")):
		categories = message.content.split(" ")
		categories = categories[2:]
		for categorie in categories:
			await message.channel.send(bot.getEtatDevise(categorie))

	if (message.content.startswith(".get list devises")):
		listDevises = bot.getListDevises()
		await message.channel.send(listDevises)

	if (message.content.startswith(".get price")):
		categories = message.content.split(" ")
		if (len(categories) == 3):
			await message.channel.send(bot.getPriceForDevise(categories[2]))

	if (message.content.startswith(".bot commands help")):
		data = "Liste des commandes:\n.create trade botName devise startingPrice\n.get devise\n.get list devises\n"
		await message.channel.send(data)

if __name__ == '__main__':
	import sys
	try:
		TOKEN = bot_token
	except:
		print('USAGE: python3 bot.py TOKENBOT')
		sys.exit(1)
	while (True):
		try:
			print("Lancement du bot en cours...")
			Client.run(TOKEN)
		except:
			pass
