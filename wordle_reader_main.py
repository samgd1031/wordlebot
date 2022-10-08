from genericpath import isfile
import discord
import logging, logging.handlers
import datetime as dt
import os
import json
import sys

from src.wordle_client.wordle_client import WordleClient


def log_namer(default_name):
    # This will be called when doing the log rotation
    # default_name is the original name the logger 
    base_filename, ext, date = default_name.split(".")
    return f"{base_filename}.{date}.{ext}"

# main part of code that runs when script is called
if __name__ == '__main__':
    # set up logger
    logfile = f"./logs/wordlebot.log"
    fmtr = logging.Formatter(fmt="%(asctime)s\t%(levelname)s:\t%(name)s\t%(message)s", datefmt="%Y-%m-%dT%H:%M:%S%z")
    file_h = logging.handlers.TimedRotatingFileHandler(filename=logfile, when="midnight", backupCount=30)  # save 30 days of backups
    file_h.setFormatter(fmtr)
    file_h.suffix = "_%Y%m%d"
    file_h.namer = log_namer

    stream_h = logging.StreamHandler(stream=sys.stdout)
    stream_h.setFormatter(fmtr)
    
    logging.basicConfig(
        level=logging.INFO,
        handlers=[stream_h, file_h]
        )
    
    logger = logging.getLogger(__name__)
    logger.info('Startup...logging configured successfully.')

    # set up discord intents
    intents = discord.Intents.default()
    intents.message_content = True

    # connect to discord & mongo
    logger.info("Creating WordleClient...")
    try:
        client = WordleClient(intents=intents, 
                                mongo_uri=os.environ["MONGO_URI"], 
                                mongo_db=os.environ["MONGO_DATABASE"])
        logger.info('WordleClient setup successful.')
    except BaseException as err:
        logger.exception("Client setup unsuccessful, see traceback below.")
        raise

    # run the client
    logger.info('Starting discord client.')
    client.run(os.environ["DISCORD_TOKEN"], log_formatter=fmtr)