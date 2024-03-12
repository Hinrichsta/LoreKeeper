import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import os
from Discord.cogs.commands import MoneyBags

def create_bot():
    load_dotenv('LoreKeeper/.env')

    Intents = discord.Intents.default()
    Intents.message_content = True
    #LoreKeeper_bot = discord.Client(intents=Intents)

    LoreKeeper_bot = commands.Bot(command_prefix='/', intents=Intents)
    @LoreKeeper_bot.event
    async def on_ready():
        print(f"Logged in as {LoreKeeper_bot.user} (ID: {LoreKeeper_bot.user.id})")
        print("----------")

    loop = asyncio.new_event_loop()
    loop.run_until_complete(LoreKeeper_bot.add_cog(MoneyBags(LoreKeeper_bot)))

    LoreKeeper_bot.run(os.getenv('DISCORD_TOKEN'))










