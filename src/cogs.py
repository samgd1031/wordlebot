import discord
from discord.ext import commands
import pymongo
import src.util as util
import os
from src.wordle_result import WordleResult

"""Listens for wordle results and sends results to mongoDB"""
class WordleUtilCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__()

        # create pymongo client
        self.mclient = pymongo.MongoClient(os.environ['MONGO_URI'])
        self.db = self.mclient["word_games"]
        self.results = self.db['wordle']
        self.players = self.db["wordle_players"]

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        """Listen to messages to see if anything fits the wordle pattern"""
        if msg.author == self.bot.user:
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
                                        update={"$addToSet":{"channel":msg.channel.id}})
            # send reply to channel
            await msg.channel.send(wr)