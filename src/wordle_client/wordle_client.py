import discord
from discord.ext import tasks
from pymongo import MongoClient
import pymongo
import pymongo.errors
from src.wordle_result.wordle_result import WordleResult
from src.util.util import *
import logging
import datetime as dt
from zoneinfo import ZoneInfo


logger = logging.getLogger(__name__)


# class describing the bot client
class WordleClient(discord.Client):

    # set up client with connection to mongoDB
    def __init__(self, *, intents: discord.Intents, mongo_uri, mongo_db, discord_channel, **options) -> None:
        self.mongo_client = MongoClient(mongo_uri)
        self.mongo_db = self.mongo_client[mongo_db]
        self.result_collection = self.mongo_db["wordle"]
        self.player_collection = self.mongo_db["wordle_players"]
        self.channel_id = discord_channel
        logger.info(f'Connected to MongoDB. Using database: {mongo_db}')
        super().__init__(intents=intents, **options)

    # notify bot owner that login is successful
    async def on_ready(self):
        logger.info(f"Logged on to Discord as {self.user}")
        self.daily_report.start()

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
                response = self.handle_valid_wordles(message)
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

            case "!mystats":
                logger.debug('got "mystats" command')
                player = {'name': message.author.name, 'discriminator':int(message.author.discriminator)}
                doc = self.player_collection.find_one({"player":player})
                if not doc:
                    await message.channel.send(f"No data found for {message.author.name}#{message.author.discriminator}.  Add some Wordles!")
                else:
                    resp = f"All-time stats for {message.author.name}#{message.author.discriminator}:\n" + \
                            f"Puzzles Played: {doc['n_played']}\n" +\
                            f"Current streak: {doc['streak']['current']} days\n" + \
                            f"Best streak:    {doc['streak']['max']} days\n"
                    nguess = ['X','1','2','3','4','5','6']
                    for ii, g in enumerate(nguess):
                        if str(ii) in doc["guess_totals"].keys():
                            resp += f"\t{g}: {doc['guess_totals'][str(ii)]}\n"
                        else:
                            resp += f"\t{g}: 0\n"
                
                await message.channel.send(resp)

            case "!help":
                logger.debug('got "help" command')
                resp =  "~WordleBot Commands~\n" + \
                        "https://github.com/samgd1031/wordle_stats\n" + \
                        "!help -   Show help\n" + \
                        "!getpuzzle wordle_###   -   Get your result for puzzle ###\n" + \
                        "!mystats   -   Get your all-time stats"
                await message.channel.send(resp)

            case other:
                logger.debug('got unrecognized command')
                message.channel.send(f'Command "{content[0]}" not recognized.')

    # figures out stuff when a player adds a new wordle message
    # updates their user stat totals, streak, etc. too
    def handle_valid_wordles(self, message: discord.Message) -> str:
        wr = WordleResult(wordle_message_to_dict(message))
        # send to database
        try:
            # updates to user stats
            filt = {'player': {'name':message.author.name, 
                               'discriminator': message.author.discriminator}}
            # always increment guess total and total puzzles played
            # also always replace last puzzle
            newval = { '$inc' : { f"guess_totals.{wr.num_guesses}" : 1, "n_played": 1},
                        '$set' : {'last_puzzle': [wr.puzzle, wr.dt]}
                        }

            # try to get existing user stats so that streak can be checked
            current_stats = self.player_collection.find_one(filt)
            if current_stats:
                last_puzzle_num = int(current_stats["last_puzzle"][0]['number'])
                new_puzzle_num = int(wr.puzzle['number'])
                streak = (new_puzzle_num - last_puzzle_num) == 1

                if streak & wr.solved:  # add one to current streak, and update longest all-time streak if necessary
                    newval["$inc"]["streak.current"] = 1
                    newval['$set']["streak.max"] = max(current_stats["streak"]["current"]+1, current_stats["streak"]["max"])
                else:  # if puzzle was failed, streak is zero, if solved, streak is 1
                    newval["$set"]["streak.current"] = 1 if wr.solved else 0


            else:  # new player
                if wr.solved:
                    newval["$inc"]["streak.current"] = 1
                    newval["$inc"]["streak.max"] = 1
                else:
                    newval["$set"]["streak"] = 0

            self.result_collection.insert_one(wr.to_dict())  # wordle result
            self.player_collection.update_one(filt, newval, upsert=True) # player stats
            response = wr.__repr__()
        except pymongo.errors.DuplicateKeyError:
            response = f"Duplicate entry for {wr.puzzle['type']} {wr.puzzle['number']}, not added to database."

        return response

    # send a report message once a day with the winners from the day before
    @tasks.loop(time=dt.time(12,0,0, tzinfo=ZoneInfo("America/Los_Angeles")))
    async def daily_report(self):
        # get latest puzzle number
        today = dt.datetime.now(tz=ZoneInfo("America/Los_Angeles")).replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday = today - dt.timedelta(days=1.0)
        logger.info(f'Calculating daily winners for {yesterday.date()}')
        
        # get ranking
        ranked, puzzle = get_daily_winners(yesterday, self.result_collection)

        # send message to discord (unless there are no entries)
        if not ranked:
            logger.info(f'No wordle entries found for {yesterday.date()}')
        else:
            msg = f"```--- Daily Competition for Wordle {puzzle} ({yesterday.date().strftime('%m/%d/%Y')}) ---\n"
            for person in ranked:
                msg += f"{person[2]}. {person[0]:16} - {person[1]}\n"
            msg += "```"

            logger.debug(msg)
            chan = await self.fetch_channel(self.channel_id)
            await chan.send(msg)
