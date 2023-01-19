import discord
from discord.ext import commands
import os
from src.cogs import WordleUtilCog
import src.util as util


class Wordlebot(commands.Bot):
    def __init__(self, *, intents: discord.Intents, **options) -> None:
        super().__init__(intents=intents, **options, command_prefix='!')

    async def setup_hook(self) -> None:
        await bot.add_cog(WordleUtilCog(bot))
        await self.tree.sync()

    async def on_ready(self):
        print("logged in")


# set up the bot
intents = discord.Intents.all()
bot = Wordlebot(intents=intents)

# slash commands for doing stuff
@bot.tree.command(name="hello")
async def hello(itx : discord.Interaction):
    """Says hello"""
    await itx.response.send_message(f"Hello {itx.user.name}", ephemeral=True)

@bot.tree.command(name="get_puzzle")
async def get_puzzle(itx: discord.Interaction, puzzle_num: int):
    """Get the ranking for a given puzzle number"""

    ucog = bot.get_cog("WordleUtilCog")
    entries = ucog.get_puzzle_entries(puzzle_num, itx.guild_id)

    # sort entries
    entries = sorted(entries, key=lambda d: d['num_guesses'])

    # build response
    resp = util.print_daily_winners(entries, puzzle_num)

    await itx.response.send_message(resp)

# run the bot
bot.run(token=os.environ["DISCORD_TOKEN"])