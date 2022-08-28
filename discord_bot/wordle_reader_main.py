
import discord
import json

from wordle_client import WordleClient


# main part of code that runs when script is called
if __name__ == '__main__':
    intents = discord.Intents.default()
    intents.message_content = True

    with open('config.json') as cfg:
        config = json.load(cfg)

    client = WordleClient(intents=intents)
    client.run(config["token"])