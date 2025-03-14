import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

class Settings(commands.Cog, name="settings"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="activate", description="Can activate a feature within the bot"
    )
    async def activate(self, context: Context) -> None:

        await context.send(embed=embed)

async def setup(bot) -> None:
    await bot.add_cog(Settings(bot))