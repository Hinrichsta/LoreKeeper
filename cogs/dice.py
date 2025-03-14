import random
import re

import discord
from random import randint
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class DiceRoller(commands.Cog, name="Dice Roller"):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    pattern1 = re.compile(r"\(\D\w+\)")
    pattern2 = re.compile(r"\d+d\d+")
    pattern3 = re.compile(r"\d+d\d+kh\d+")
    pattern4 = re.compile(r"\d+d\d+kl\d+")
    pattern5 = re.compile(r"\(\d+d\d+\)")
    
    patterns = {
        "name": pattern1,
        "base": pattern2,
        "adv": pattern3,
        "disadv": pattern4,
        "groups": pattern5
    }

    @commands.hybrid_command(name="roll", aliases=["r"], description="List all commands the bot has loaded.")
    async def roll(self, context: Context, roll: str) -> None:
        """
        Roll the dice and see what you get.

        :param context: The hybrid command context.
        :param roll: The formula for the requested roll.
        """

        dice_rolled = roll.split("d")
        dice_outcome = "("
        dice_total = 0
        for i in range(int(dice_rolled[0])):
            roll = randint(1,int(dice_rolled[1]))
            if (i == (int(dice_rolled[0])-1)):
                dice_outcome += f"{roll})"

            else:
                dice_outcome += f"{roll}, "

            dice_total += roll
        

        embed = discord.Embed(
            title=f"rolling {dice_rolled[0]}d{dice_rolled[1]}",
            description=f"{dice_outcome} = {dice_total}",
        )

        await context.send(embed=embed)




async def setup(bot) -> None:
    await bot.add_cog(DiceRoller(bot))