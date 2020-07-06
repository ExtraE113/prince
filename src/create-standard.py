"""Creates a standard 52-card deck and puts it in cards.json"""

from tinydb import TinyDB, where

# todo the clean way to do this would be to have a base class and override it and whatever
#  but this is quick and dirty so I'm not going to bother.

standard = TinyDB("../resources/cards.json")

exists = len(standard.search(where("name") == "standard")) > 0

if exists:
	raise Exception('A deck with that name already exists ("standard")')

deck = []
for j in ["Hearts", "Diamonds", "Clubs", "Spades"]:
	# todo should be a generator, but whatever
	for i in range(1, 14):
		if i == 0:
			i = "Ace"
		elif i == 11:
			i = "Jack"
		elif i == 12:
			i = "Queen"
		elif i == 13:
			i = "King"

		deck.append(f"{i} of {j}")

standard.insert({"cards": deck, "name": "standard"})
