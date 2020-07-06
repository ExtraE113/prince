import random
import sys
from collections import defaultdict

import discord
from tinydb import TinyDB, where
from tinydb.operations import increment, delete
from tinydb.storages import MemoryStorage
import os.path
import os

custom_cards_defined = os.path.exists("../resources/custom-cards.json")

client = discord.Client()
db = TinyDB("../resources/db.json")


cards = TinyDB("../resources/cards.json" if not custom_cards_defined else "../resources/custom-cards.json")

TOKEN = os.getenv("TOKEN")


# helper function to convert user input to bool
def stb(s: str):
	# todo move this list to config
	return s.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'yep', 'certainly', 'uh-huh', 'you-bet']


for i in cards.all():
	if "custom-shuffler" in i and False:
		trust_str = input(
			f"The {i['name']} deck contains a custom shuffler. A malicious custom shuffler can compromise (hack) your computer. Do you trust the person who gave you your deck? If you are unsure you should answer no.\n")
		trust = stb(trust_str)
		if not trust:
			sys.exit()


@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith('!draw'):
		chan = message.channel.id
		try:
			deck = db.search(where('chan') == chan)[0]
		except IndexError:
			msg = "There isn't a deck in this channel yet. Create one with !createdeck"
			await message.channel.send(msg)
			return

		try:
			card_number = deck["index"]
			card = deck['deck'][card_number]
			card = card.replace("\n", "\n> ")
			msg = f"You drew \n> {card}"
			db.update(increment("index"), where("chan") == chan)
		except IndexError:
			msg = "No more cards!"

		await message.channel.send(msg)
		return

	if message.content.startswith('!createdeck'):
		chan = message.channel.id
		str_args = message.content.split(" ")[1:]

		args = defaultdict(lambda: "False")
		for i in str_args:
			i = i.split("=")
			arg = i[0][2:]
			data = i[1] if len(i) > 1 else "True"
			args[arg] = data

		exists = len(db.search(where("chan") == chan)) > 0

		print(args)

		if exists and not stb(args["delete-old"]):
			await message.channel.send(
				"A deck already exists in this channel. Add --delete-old to your request to delete it and proceed.")
			return
		elif exists and stb(args["delete-old"]):
			db.update(delete("chan"), where("chan") == chan)

		deck_name = args["deck"] if "deck" in args else "standard"
		deck_name = args["name"] if "name" in args else deck_name

		try:
			deck = cards.search(where("name") == deck_name)[0]["cards"]
		except IndexError:
			await message.channel.send(f"You don't have a deck named {deck_name}. "
									   f"Check your spelling, or ask your bot administrator to check their `cards.json` "
									   f"or `custom-cards.json` file.")
			return

		default_shuffler = """def default_shuffler(deck):
	random.shuffle(deck)
	return deck
global shuffler_fun
shuffler_fun = default_shuffler"""

		try:
			shuffle = cards.search(where("name") == deck_name)[0]["custom-shuffler"]
		except KeyError:
			shuffle = default_shuffler

		global shuffler_fun

		exec(shuffle, globals(), locals())

		deck = shuffler_fun(deck)


		db.insert({"chan": chan, "deck": deck, "index": 0})
		await message.channel.send(f"{deck_name} deck created!")


client.run(TOKEN)
