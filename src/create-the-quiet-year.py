"""Creates a The Quiet Year deck and adds it to custom-cards.json.
You can buy a pdf of the game online and then copy and paste the Oracle into raw-cards.txt"""
import random

from tinydb import TinyDB, where
import re

standard = TinyDB("../resources/custom-cards.json")
exists = len(standard.search(where("name") == "the-quiet-year")) > 0
if exists:
	raise Exception('A deck with that name already exists ("the-quiet-year")')

deck = []

with open("raw-cards.txt", mode="r", encoding='utf-8') as fp:
	lines = fp.readlines()
	int_season = -1
	for season in lines:
		# split by the card's pre-text which is the value of a card in a 52 card deck--
		# 	either A, 2-9, 10, J, Q, K
		# Works because the text file is formatted AFirst card text2Second card text3Third card text
		# 	So we can match for an identifier (A, 2-9, 10, J, Q, K)
		# 	followed by a capital letter (the start of the next card's text)
		# Also matches newlines because these appear at the beginning of seasons.
		int_season += 1
		for card in re.split("((10|[2-9]|A|J|Q|K)(?=[A-Z])|\n)", season):
			if card is None or len(card) < 3:  # skip the identifiers, which also make it into the list
				continue
			card = card.replace("or...", "\nor..\n")

			if card.endswith("Spring"):
				card = card[:-len("Spring")]
			elif card.endswith("Summer"):
				card = card[:-len("Summer")]
			elif card.endswith("Winter"):
				card = card[:-len("Winter")]
			elif card.endswith("Autumn"):
				card = card[:-len("Autumn")]

			seasons = ["Spring", "Summer", "Autumn", "Winter"]

			deck.append(seasons[int_season] + ": " + card)


shuffle = """def shuffler(deck):
	out = []

	spring = deck[0:13]
	summer = deck[13:26]
	autumn = deck[26:39]
	winter = deck[39:52]

	random.shuffle(spring)
	random.shuffle(summer)
	random.shuffle(autumn)
	random.shuffle(winter)

	out += spring
	out += summer
	out += autumn
	out += winter

	return out
global shuffler_fun
shuffler_fun = shuffler"""


standard.insert({"cards": deck, "name": "the-quiet-year", "custom-shuffler": shuffle})

# todo should be part of custom shuffler
shuffle = """def shuffler(deck):
	out = []

	spring = deck[0:13]
	summer = deck[13:26]
	for k in summer:
		if "Summer is fleeting. Discard" in k:
			summer.remove(k)
	autumn = deck[26:39]
	winter = deck[39:52]
	for k in winter:
		if "The Frost Shepherds arrive" in k:
			winter.remove(k)

	random.shuffle(spring)
	random.shuffle(summer)
	random.shuffle(autumn)
	random.shuffle(winter)
	
	spring = spring[4:]
	summer = summer[3:]
	autumn = autumn[4:]
	winter = winter[4:]
	
	winter.append("The Frost Shepherds arrive. The game is over.")
	
	random.shuffle(winter)
	
	out += spring
	out += summer
	out += autumn
	out += winter

	return out
global shuffler_fun
shuffler_fun = shuffler"""


standard.insert({"cards": deck, "name": "the-quiet-year-fleeting", "custom-shuffler": shuffle})
