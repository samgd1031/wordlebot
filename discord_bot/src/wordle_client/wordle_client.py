import discord

from wordle_result.wordle_result import WordleResult
from util.util import *

# class describing the bot client
class WordleClient(discord.Client):
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
            response = wr.__repr__()
            await message.channel.send(response)
        else:
            print(f"{message.created_at}: {message.author} - \"{message.content}\"")
            print("\tNot valid Wordle Result!")