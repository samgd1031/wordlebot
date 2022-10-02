import discord
import json
import logging
import datetime as dt

from wordle_client.wordle_client import WordleClient

# main part of code that runs when script is called
if __name__ == '__main__':
    # set up logger
    logfile = f"./logs/wordlebot_{dt.datetime.utcnow().strftime('%m_%d_%Y_UTC')}.log"
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename=logfile,
        format="%(asctime)s\t%(levelname)s:\t%(name)s\t%(message)s",
        datefmt="%m/%d/%Y %H:%M:%S %z",
        level=logging.INFO)

    # set up discord intents
    intents = discord.Intents.default()
    intents.message_content = True

    # read configuration parameters (Discord & Mongo connection info)
    with open('config.json') as cfg:
        config = json.load(cfg)

    # connect to discord & mongo
    client = WordleClient(intents=intents, 
                            mongo_uri=config["MONGO_URI"], 
                            mongo_db=config["MONGO_DATABASE"], 
                            mongo_col=config["MONGO_COLLECTION"])
    logger.info('WordleClient setup.  Starting client...')
    client.run(config["DISCORD_TOKEN"])