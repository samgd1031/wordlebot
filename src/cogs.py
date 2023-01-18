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
            wr = WordleResult(util.wordle_message_to_dict(msg))
            await msg.channel.send(wr)