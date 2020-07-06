import discord
from tinydb import TinyDB, where

client = discord.Client()
db = TinyDB("../resources/db.json")
config = TinyDB("../resources/config.json")
config_data = config.table("config")

TOKEN = config_data.all()[0]["TOKEN"]


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!draw'):
        chan = message.channel
        deck = db.search(where('chan') == chan)
        if len(deck) == 0:
            await message.channel.send("There isn't a deck in this channel yet. Create one with !createdeck")



client.run(TOKEN)
