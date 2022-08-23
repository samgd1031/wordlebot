
import discord
import json


# class describing the bot client
class WordleClient(discord.Client):
    # notify bot owner that login is successful
    async def on_ready(self):
        print(f"Logged on as {self.user}")

    # for now, simply print discord message to console
    # later will need to add code that parses wordle messages and does something interesting with them
    async def on_message(self, message):
        print(f"Message from {message.author} - {message.content}")



# main part of code that runs when script is called
if __name__ == '__main__':
    intents = discord.Intents.default()
    intents.message_content = True

    with open('config.json') as cfg:
        config = json.load(cfg)

    client = WordleClient(intents=intents)
    client.run(config["token"])