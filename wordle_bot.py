import discord
from discord.ext import commands
import os
from src.cogs import WordleUtilCog


class Wordlebot(commands.Bot):
    def __init__(self, *, intents: discord.Intents, **options) -> None:
        super().__init__(intents=intents, **options, command_prefix='!')

    async def setup_hook(self) -> None:
        await bot.add_cog(WordleUtilCog(bot))
        #self.tree.copy_global_to(guild=discord.Object(id=1011135985460985906))
        #await self.tree.sync()

    async def on_ready(self):
        print("logged in")

intents = discord.Intents.all()
bot = Wordlebot(intents=intents)


@bot.tree.command(name="hello")
async def test2(itx : discord.Interaction):
    """Says hello"""
    await itx.response.send_message(f"Hello {itx.user.name}", ephemeral=True)



bot.run(token=os.environ["DISCORD_TOKEN"])