import discord
from pymongo import MongoClient
import pymongo
import pymongo.errors
from src.wordle_result.wordle_result import WordleResult
from src.util.util import *
import logging


logger = logging.getLogger(__name__)


# class describing the bot client
class WordleClient(discord.Client):

    # set up client with connection to mongoDB
    def __init__(self, *, intents: discord.Intents, mongo_uri, mongo_db, **options) -> None:
        self.mongo_client = MongoClient(mongo_uri)
        self.mongo_db = self.mongo_client[mongo_db]
        self.result_collection = self.mongo_db["wordle"]
        self.player_collection = self.mongo_db["wordle_players"]
        logger.info(f'Connected to MongoDB. Using database: {mongo_db}')
        super().__init__(intents=intents, **options)

    # notify bot owner that login is successful
    async def on_ready(self):
        logger.info(f"Logged on to Discord as {self.user}")

    # if valid wordle message, parse and have the bot send a message back
    # otherwise just print the invalid message to console (this behavior can probably be removed eventually)
    # instead of printing to console this should also be logged
    async def on_message(self, message: discord.Message):
        # ignore messages from this bot (it should never send a wordle message but just in case)
        if message.author == self.user:
            return
        
        # check if command (starts with '!')
        if message.content[0] == '!':
            await self._handle_commands(message)

        else: # non command message
            # checks if valid wordle
            content = message.content.split("\n")
            if is_valid_wordle(content[0]):
                wr = WordleResult(wordle_message_to_dict(message))
                # send to database
                try:
                    self.result_collection.insert_one(wr.to_dict())  # wordle result
                    filt = {'player': f"{message.author.name}_{message.author.discriminator}"}
                    newval = { '$inc' : { f"guess_totals.{wr.num_guesses}" : 1}}
                    self.player_collection.update_one(filt, newval, upsert=True)
                    response = wr.__repr__()
                except pymongo.errors.DuplicateKeyError:
                    response = f"Duplicate entry for {wr.puzzle_number}, not added to database."

                await message.channel.send(response)
            else:
                logger.debug(f"{message.author} - \"{message.content}\" - Not a Wordle!")

    async def _handle_commands(self, message: discord.Message):
        content = message.content.split(" ")

        match content[0]:
            case "!getpuzzle":  # get results for a single puzzle belonging to the user
                logger.debug('got "getpuzzle" command')
                if len(content) != 2:
                    await message.channel.send("Usage: !getpuzzle wordle_###")
                    return
                
                # try to find this puzzle with this user in mongoDB
                id = f"{message.author.name}_{message.author.discriminator}_{content[1]}"
                result = self.result_collection.find_one({"_id":id})
                if result:
                    result = WordleResult(result)
                    await message.channel.send(result)
                else:
                    logger.debug(f'{content[1]} not found!')
                    await message.channel.send(f'{content[1]} not found!')

            case "!help":
                logger.debug('got "help" command')
                resp =  "~WordleBot Commands~\n" + \
                        "!help -   Show help\n" + \
                        "!getpuzzle wordle_###   -   Get your result for puzzle ###"
                await message.channel.send(resp)

            case other:
                logger.debug('got unrecognized command')
                message.channel.send(f'Command "{content[0]}" not recognized.')