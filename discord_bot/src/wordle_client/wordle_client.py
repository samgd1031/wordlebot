import discord
from pymongo import MongoClient
import pymongo
import pymongo.errors
from wordle_result.wordle_result import WordleResult
from util.util import *
import os

# class describing the bot client
class WordleClient(discord.Client):

    # set up client with connection to mongoDB
    def __init__(self, *, intents: discord.Intents, mongo_uri, mongo_db, mongo_col, **options) -> None:
        self.mongo_client = MongoClient(mongo_uri)
        self.mongo_db = self.mongo_client[mongo_db]
        self.mongo_collection = self.mongo_db[mongo_col]
        print(f'Connected to MongoDB. Collection: {mongo_col} in Database: {mongo_db}')
        super().__init__(intents=intents, **options)

    # notify bot owner that login is successful
    async def on_ready(self):
        print(f"Logged on as {self.user}")

    # if valid wordle message, parse and have the bot send a message back
    # otherwise just print the invalid message to console (this behavior can probably be removed eventually)
    # instead of printing to console this should also be logged
    async def on_message(self, message: discord.Message):
        # ignore messages from this bot (it should never send a wordle message but just in case)
        if message.author == self.user:
            return
            
        content = message.content.split("\n")
        if is_valid_wordle(content[0]):
            wr = WordleResult(message, content[0])

            # send to database
            try:
                self.mongo_collection.insert_one(wr.to_dict())
                response = wr.__repr__()
            except pymongo.errors.DuplicateKeyError:
                response = f"Duplicate entry for {wr.puzzle_number} added to database.)"

            await message.channel.send(response)
        else:
            print(f"{message.created_at}: {message.author} - \"{message.content}\"")
            print("\tNot valid Wordle Result!")