import discord
from discord.ext import commands
import os
import src.util as util


class Wordlebot(commands.Bot):
    def __init__(self, *, intents: discord.Intents, **options) -> None:
        super().__init__(intents=intents, **options, command_prefix='!')
        self.remove_command("help")

    async def setup_hook(self) -> None:
        await self.load_extensions()

    async def load_extensions(self):
        """load cogs"""
        for file in os.listdir("./src/cogs"):
            if file.endswith(".py"):
                await self.load_extension(f"src.cogs.{file[:-3]}")

    async def on_ready(self):
        print("logged in")


if __name__ == '__main__':
    # set up the bot
    intents = discord.Intents.all()
    bot = Wordlebot(intents=intents)
    # run the bot
    bot.run(token=os.environ["DISCORD_TOKEN"])