import discord
from discord.ext import commands, tasks
import pymongo
import src.util as util
import os
from src.wordle_result import WordleResult
from zoneinfo import ZoneInfo
import datetime as dt

"""Listens for wordle results and sends results to mongoDB"""
class WordleUtils(commands.Cog):
    def __init__(self, client) -> None:
        super().__init__()
        self.client = client
        # create pymongo client
        self.mclient = pymongo.MongoClient(os.environ['MONGO_URI'])
        self.db = self.mclient["word_games"]
        self.results = self.db['wordle']
        #self.players = self.db["wordle_players"] # TODO, add persistent player stats
        self.data = self.db["wordlebot_data"]
        self.daily_report.start()


    def get_puzzle_entries(self, puzzle_num: int, guild_id: int):
        """Given a puzzle number, get the entries for that puzzle
            Optionally filter by guild_id
            Results will be sorted by number of guesses (low to high)
        """
        # first get all entries for the puzzle
        docs = self.results.find({"puzzle":{"type":"Wordle", "number":puzzle_num}})
        docs = list(docs)

        # then filter to just ones in the guild the command originated from
        if guild_id:
            docs = [ doc for doc in docs if guild_id in doc['guild'] ]

        # sort
        docs = sorted(docs, key=lambda d: d['num_guesses'])
        return docs


    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        """Listen to messages to see if anything fits the wordle pattern"""
        if msg.author == self.client.user:
            return
        content = msg.content.split("\n")
        if util.is_valid_wordle(content[0]):
            wordle_dict = util.wordle_message_to_dict(msg)
            wr = WordleResult(wordle_dict)
            # add the result to mongoDB
            # check if the result exists and append the channel (if not duplicate)
            result = self.results.find_one(filter={"_id":wordle_dict["_id"]})
            if result: # exists, append channel
                self.results.update_one(filter={"_id":wordle_dict["_id"]},
                                        update={"$addToSet":{"guild":msg.guild.id if msg.guild else 0,
                                                             "channel":msg.channel.id}})
            else:  # add a new document
                self.results.insert_one(wordle_dict)
            # send reply to channel
            await msg.channel.send(wr)


    @tasks.loop(time=dt.time(12,0,0, tzinfo=ZoneInfo("America/Los_Angeles")))
    async def daily_report(self):
        """Get results for the previous day and make a post in the appropriate channels at noon pacific time"""
        doc = self.data.find_one(filter={"_id":"wordle"})
        puzzle = doc['number']

        entries = self.get_puzzle_entries(puzzle, None)

        # sort by server
        grouped_entries = {}
        for e in entries:
            for ii, guild in enumerate(e['guild']):
                if guild == 0: # skip dm'd results
                    continue
                if guild not in grouped_entries:
                    grouped_entries[guild] = {"entries":[e], "channel":e["channel"][ii]}
                else:
                    grouped_entries[guild]["entries"].append(e)

        # send a result message for each guild
        for gid in grouped_entries.keys():
            resp = util.print_daily_winners(grouped_entries[gid]["entries"], puzzle)
            channel = self.client.get_channel(grouped_entries[gid]["channel"])
            await channel.send(resp)

        # increment puzzle number for the next day
        self.data.update_one(filter={"_id":"wordle"},
                             update={"$inc":{"number": 1}})

    @daily_report.before_loop
    async def before_daily(self):
        await self.client.wait_until_ready()

    @commands.hybrid_command()
    async def get_puzzle(self, ctx: commands.Context, puzzle_number):
        """Get the rankings for a given wordle puzzle number"""
        results = self.get_puzzle_entries(int(puzzle_number), guild_id=ctx.guild.id)
        resp = util.print_daily_winners(results, puzzle_number)
        await ctx.send(resp)


async def setup(client: commands.Bot):
    await client.add_cog(WordleUtils(client=client))