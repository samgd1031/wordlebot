
import discord
import json
import re

from wordle_result import WordleResult


# class describing the bot client
class WordleClient(discord.Client):
    # notify bot owner that login is successful
    async def on_ready(self):
        print(f"Logged on as {self.user}")

    # for now, simply print discord message to console
    # later will need to add code that parses wordle messages and does something interesting with them
    async def on_message(self, message):
        print(f"Message from {message.author} - {message.content}")
        if self.is_valid_wordle(message):
            print("\tValid Wordle Result!")
        else:
            print("\tNot valid Wordle Result!")

    # check if a message string is a valid wordle result
    def is_valid_wordle(self, message) -> bool:
        content = message.content.split("\n")

        isWordle = re.match(r"Wordle \d* [\dX]/6\*?",
                            content[0])
        
        if isWordle:
            wr = WordleResult(message.author, content[0])
            print(wr)
            return True
        else:
            return False


# main part of code that runs when script is called
if __name__ == '__main__':
    intents = discord.Intents.default()
    intents.message_content = True

    with open('config.json') as cfg:
        config = json.load(cfg)

    client = WordleClient(intents=intents)
    client.run(config["token"])