import discord
from discord.ext import commands

class HelpCommand(commands.HelpCommand):
    def __init__(self, prefix, **options) -> None:
        self.prefix = prefix
        super().__init__(**options)

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Wordlebot Help")
        for cog, cmds in mapping.items():
            if cog is None:
                continue
            cmds = await self.filter_commands(cmds, sort=True)
            if len(cmds) > 0:
                embed.add_field(name=f"{cog.qualified_name}",
                                value= f"{len(cmds)} commands")


        embed.set_footer(text=f"Run {self.prefix}{self.invoked_with} [name] to learn more about its commands")
        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_cog_help(self, cog: commands.Cog, /) -> None:
        cmds = await self.filter_commands(cog.get_commands(), sort=True)
        cmds = "\n".join(f"{cmd.name}: {cmd.help}" for cmd in cmds)
        embed = discord.Embed(title=f"{cog.qualified_name} Help")
        embed.description = f"```{cmds}```"
        await self.get_destination().send(embed=embed)

async def setup(client: commands.Bot):
    client._default_help_command = client.help_command
    client.help_command = HelpCommand(prefix=client.command_prefix)