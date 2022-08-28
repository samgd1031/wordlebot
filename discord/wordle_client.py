import re
import discord

from wordle_result import WordleResult

# class describing the bot client
class WordleClient(discord.Client):
    # notify bot owner that login is successful
    async def on_ready(self):
        print(f"Logged on as {self.user}")

    # if valid wordle message, parse and have the bot send a message back
    # otherwise just print the invalid message to console (this behavior can probably be removed eventually)
    # instead of printing to console this should also be logged
    async def on_message(self, message):
        # ignore messages from this bot (it should never send a wordle message but just in case)
        if message.author == self.user:
            return

        if self.is_valid_wordle(message):
            content = message.content.split("\n")
            wr = WordleResult(message, content[0])
            response = wr.__repr__()
            await message.channel.send(response)
        else:
            print(f"{message.created_at}: {message.author} - \"{message.content}\"")
            print("\tNot valid Wordle Result!")

    # check if a message string is a valid wordle result
    def is_valid_wordle(self, message) -> bool:
        content = message.content.split("\n")

        isWordle = re.match(r"Wordle \d* [1-6X]/6\*?",
                            content[0])
        
        if isWordle:
            return True
        else:
            return False