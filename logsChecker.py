import discord
import asyncio
import time
from random import randint, choice, SystemRandom
import logging
import re
import os

Client = discord.Client(command_prefix="")

@Client.event
async def on_message(message):
	if (Client.user.id == message.author.id):
		return
	if (message.content.startswith("check logs")):
		await message.channel.send("Chargement des logs en cours...")
		with open("./logs/BTCBUSD.log", "r") as f:
			logs = f.readlines()
		await message.channel.send(logs)

if __name__ == '__main__':
	import sys
	try:
		TOKEN = "OTUzMDQ1MDI3NzQxODk2NzA0.Yi-2WQ.ZjolXokgZwdM34NUsEldm5BxF0Q"
	except:
		print('USAGE: python3 bot.py TOKENBOT')
		sys.exit(1)
	while (True):
		try:
			print("Lancement du bot en cours...")
			Client.run(TOKEN)
		except:
			pass


"""
On achète les valeurs en dessous des valeurs de support
On les gardes tant qu'on atteint pas les résistance on gardes
Si ça arrive à 159 tu vend pas
Si ça fait 160 / 158 etc, que ça rebondit tu revend cette valeurs
"""
