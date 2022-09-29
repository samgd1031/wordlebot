import discord
import json

from wordle_client.wordle_client import WordleClient
from dotenv import load_dotenv


# main part of code that runs when script is called
if __name__ == '__main__':
    intents = discord.Intents.default()
    intents.message_content = True

    with open('config.json') as cfg:
        config = json.load(cfg)


    load_dotenv()
    client = WordleClient(intents=intents, 
                            mongo_uri=config["MONGO_URI"], 
                            mongo_db=config["MONGO_DATABASE"], 
                            mongo_col=config["MONGO_COLLECTION"])
    client.run(config["DISCORD_TOKEN"])