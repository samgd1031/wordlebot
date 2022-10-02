from genericpath import isfile
import discord
import logging
import datetime as dt
import os
import json

from src.wordle_client.wordle_client import WordleClient

# main part of code that runs when script is called
if __name__ == '__main__':
    # set up logger
    logfile = f"./logs/wordlebot_{dt.datetime.utcnow().strftime('%m_%d_%Y_UTC')}.log"
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename=logfile,
        format="%(asctime)s\t%(levelname)s:\t%(name)s\t%(message)s",
        datefmt="%m/%d/%Y %H:%M:%S %z",
        level=logging.INFO)
    logger.info('Startup...logging configured successfully.')
    # set up discord intents
    intents = discord.Intents.default()
    intents.message_content = True

    '''
    # helps debug outside of docker container, uncomment to load env from config.json
    if os.path.isfile('config.json'):
        with open('config.json') as cfg:
            config = json.load(cfg)
            os.environ["MONGO_URI"] = config["MONGO_URI"]
            os.environ["MONGO_DATABASE"] = config["MONGO_DATABASE"]
            os.environ["MONGO_COLLECTION"] = config["MONGO_COLLECTION"]
            os.environ["DISCORD_TOKEN"] = config["DISCORD_TOKEN"]
    '''

    # connect to discord & mongo
    logger.info("Creating WordleClient...")
    try:
        client = WordleClient(intents=intents, 
                                mongo_uri=os.environ["MONGO_URI"], 
                                mongo_db=os.environ["MONGO_DATABASE"], 
                                mongo_col=os.environ["MONGO_COLLECTION"])
        logger.info('WordleClient setup successful.')
    except BaseException as err:
        logger.exception("Client setup unsuccessful, see traceback below.")
        raise

    # run the client
    logger.info('Starting discord client.')
    client.run(os.environ["DISCORD_TOKEN"])