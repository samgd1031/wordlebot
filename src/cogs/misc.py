import discord
import time
from discord.ext import commands


class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command()
    async def ping(self, ctx):
        """Get bot latency"""
        before = time.monotonic()
        before_ws = int(round(self.client.latency * 1000, 3))
        msg = await ctx.send("Pinging...")
        _ping = (time.monotonic() - before) * 1000

        embed = discord.Embed(title="Latency", description=f"```yaml\nWS:\n  - {before_ws}ms\nREST:\n  - {int(_ping)}ms\n```")
        await msg.edit(content="", embed=embed)

    @commands.hybrid_command()
    async def hello(self, ctx: commands.Context):
        """Says hello"""
        await ctx.send(f"Hello {ctx.author.name}", ephemeral=True)

    @commands.command()
    @commands.is_owner()
    async def sync_commands(self, ctx: commands.Context):
        await self.client.tree.sync()
        await ctx.send(f"synced commands globally", ephemeral= True)

    
async def setup(client: commands.Bot):
    await client.add_cog(Misc(client=client))