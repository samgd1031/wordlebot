import re
import discord

from wordle_result import WordleResult

# class describing the bot client
class WordleClient(discord.Client):
    # notify bot owner that login is successful
    async def on_ready(self):
        print(f"Logged on as {self.user}")

    # for now, simply print discord message to console
    # later will need to add code that parses wordle messages and does something interesting with them
    async def on_message(self, message):
        if self.is_valid_wordle(message):
            content = message.content.split("\n")
            wr = WordleResult(message.author, content[0])
            print(wr)
        else:
            print("\tNot valid Wordle Result!")

    # check if a message string is a valid wordle result
    def is_valid_wordle(self, message) -> bool:
        content = message.content.split("\n")

        isWordle = re.match(r"Wordle \d* [\dX]/6\*?",
                            content[0])
        
        if isWordle:
            return True
        else:
            return False