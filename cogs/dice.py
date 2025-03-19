import random
import re
import asyncio

import discord
import logging
from random import randint
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

logger = logging.getLogger("lorekeeper_bot")

# ANSI Color Codes
ansi_blue = "\u001b[0;34m"
ansi_green = "\u001b[0;32m"
ansi_red = "\u001b[0;31m"
ansi_grey = "\u001b[0;30m"
ansi_clear = "\u001b[0;0m"



class DiceRoller(commands.Cog, name="Dice Roller"):
    def __init__(self, bot) -> None:
        self.bot = bot

    def keep_roll(self, roll, keep_string: str):
        """
        Does Dice rolls (Dis)Advantage checks

        :param roll: The string of the roll that is being passed.
        :param keep_string: The string of if it is Keep Highest or Keep Lowest.
        """

        dice_size = (roll[1].split(keep_string))[0]
        dice_keep = (roll[1].split(keep_string))[1] or None
        roll_keep = []
        dice_outcome = "("
        dice_total = 0
        roll_results = []

        #Runs through the dice rolled, and puts them into a list
        for i in range(int(roll[0])):
            roll_results.append(randint(1,int(dice_size)))

        #Advantage Checks.  Will look to see if it is straight advantage, or if is a count of advantage
        if keep_string == 'kh':
            if dice_keep is not None:
                temp_list = roll_results.copy()
                for i in range(int(dice_keep)):
                    highest = 0
                    for j in range(len(temp_list)):
                        if temp_list[j] > highest:
                            highest = temp_list[j]
                    temp_list.remove(highest)
                    roll_keep.append(highest)
            else:
                roll_keep.append(max(roll_results))
        else: 
            if dice_keep is not None:
                temp_list = roll_results.copy()
                for i in range(int(dice_keep)):
                    lowest = int(dice_size)
                    for j in range(len(temp_list)):
                        if temp_list[j] < lowest:
                            lowest = temp_list[j]
                    temp_list.remove(lowest)
                    roll_keep.append(lowest)
            else:
                roll_keep.append(min(roll_results))

        for i in range(len(roll_results)):
            done_check = False
            for k in range(len(roll_keep)): #Runs through the advantage max, starting and the next number each time it is found
                if roll_results[i] == roll_keep[k]: # Checks to see if the current result equals the highest value
                    if (i == (int(roll[0])-1)):
                        if (roll_results[i] == int(dice_size)):
                            dice_outcome += f"{ansi_green}{roll_results[i]}{ansi_clear})"
                        elif (roll_results[i] == 1):
                            dice_outcome += f"{ansi_red}{roll_results[i]}{ansi_clear})"
                        else:
                            dice_outcome += f"{ansi_blue}{roll_results[i]}{ansi_clear})"
                    else:
                        if (roll_results[i] == int(dice_size)):
                            dice_outcome += f"{ansi_green}{roll_results[i]}{ansi_clear}, "
                        elif (roll_results[i] == 1):
                            dice_outcome += f"{ansi_red}{roll_results[i]}{ansi_clear}, "
                        else:
                            dice_outcome += f"{ansi_blue}{roll_results[i]}{ansi_clear}, "
                    dice_total += roll_results[i]
                    roll_keep.remove(roll_keep[k])
                    done_check = True
                    break
                
            if not done_check:
                if (i == (int(roll[0])-1)):
                    dice_outcome += f"{ansi_grey}{roll_results[i]}{ansi_clear})"
                else:
                    dice_outcome += f"{ansi_grey}{roll_results[i]}{ansi_clear}, "
        
        return dice_outcome, dice_total


    @commands.hybrid_command(name="roll", aliases=["r"], description="List all commands the bot has loaded.")
    async def roll(self, context: Context, *, roll_request: str) -> None:
        """
        Roll the dice and see what you get.

        :param context: The hybrid command context.
        :param roll: The formula for the requested roll.
        """

        #enabled = await self.bot.database.get_settings(context.guild.id)
        #self.logger.info(f"Dice check: {enabled}")
        #await asyncio.sleep(5)
        #if enabled[1] == 0:
        #    exit
        
        # Regex Patterns
        pattern_name = re.compile(r"\w+ \(\D\w+\)") # Discord Name
        pattern_base = re.compile(r"\d+d\d+") # Base Roll Pattern
        pattern_adv = re.compile(r"\d+d\d+kh") # Advantage Roll Pattern 
        pattern_disadv = re.compile(r"\d+d\d+kl") # Disadvantage Roll Pattern 
        pattern_adv_plus = re.compile(r"\d+d\d+kh\d+") # Advantage Roll Pattern for multiple highest
        pattern_disadv_plus = re.compile(r"\d+d\d+kl\d+") # Disadvantage Roll Pattern for multiple lowest
        pattern_all = re.compile(r"\d+d\d+kh\d*|\d+d\d+kl\d*|\d+d\d+") # Looks for all roll requests
        pattern_paren = re.compile(r"\(\d+\)d\d+") # Parenthesis Roll Pattern

        # Get the User's Name
        if re.match(pattern_name, context.author.display_name):
            name = context.author.display_name.split('(')[1].strip('()')
        else:
            name = context.author.display_name
        
        # Other Variables
        dice_rolled_cap = 500
        die_size_cap = 1000
        rolling_dice = True

        lower_roll_requests = roll_request.lower()
        parsed_roll_requests = re.findall(pattern_all, lower_roll_requests)
        logger.info(f"parsed_roll_requests: {parsed_roll_requests}")
        temp_request = re.sub(pattern_all, '{}', roll_request)
        logger.info(f"Subbed Request: {temp_request}")
        all_roll_formula = []
        all_roll_results = []
        all_roll_totals = []

        # start Logger
        logger.info(f"Rolling some dice for {context.author.display_name}.  Requested Roll: {roll_request}")
        if parsed_roll_requests is None or not parsed_roll_requests:
            response = f"**{name}** isn't even rolling anything... Try again"
            await context.reply(response)

        else: 
            for r in parsed_roll_requests:
                # Looks for requests using Advantage
                this_roll = r.lower()
                dice_rolled = this_roll.split("d")

                if re.match(pattern_adv, r) and rolling_dice:
                    dice_size = (dice_rolled[1].split('kh'))[0]

                    if (int(dice_rolled[0]) > dice_rolled_cap):
                        response = f"**{name}** is trying to roll to many dice.  Please try again with less"
                        rolling_dice = False
                        await context.reply(response)
                    elif (int(dice_size) > die_size_cap): 
                        response = f"**{name}** is trying to roll to large of dice.  Please try again with smaller dice"
                        rolling_dice = False
                        await context.reply(response)
                    elif (dice_rolled[1].split('kh'))[1] != '' and (int((dice_rolled[1].split('kh'))[1]) > int(dice_rolled[0])):
                        response = f"**{name}** is trying keep more dice that they are rolling.  Please try again while keeping less dice"
                        rolling_dice = False
                        await context.reply(response)
                    else:
                        dice_outcome, dice_total = self.keep_roll(dice_rolled, 'kh')
                        all_roll_formula.append(this_roll)
                        all_roll_results.append(dice_outcome)
                        all_roll_totals.append(dice_total)

                # Looks for roll requests using Disadvantage
                elif re.match(pattern_disadv, r) and rolling_dice:
                    dice_size = (dice_rolled[1].split('kl'))[0]

                    if (int(dice_rolled[0]) > dice_rolled_cap):
                        response = f"**{name}** is trying to roll to many dice.  Please try again with less"
                        rolling_dice = False
                        await context.reply(response)
                    elif (int(dice_size) > die_size_cap): 
                        response = f"**{name}** is trying to roll to large of dice.  Please try again with smaller dice"
                        rolling_dice = False
                        await context.reply(response)
                    elif (dice_rolled[1].split('kl'))[1] != '' and (int((dice_rolled[1].split('kl'))[1]) > int(dice_rolled[0])):
                        response = f"**{name}** is trying keep more dice that they are rolling.  Please try again while keeping less dice"
                        rolling_dice = False
                        await context.reply(response)
                    else:
                        dice_outcome,dice_total = self.keep_roll(dice_rolled, 'kl')
                        all_roll_formula.append(this_roll)
                        all_roll_results.append(dice_outcome)
                        all_roll_totals.append(dice_total)

                # Looks for all standard roll requests
                elif rolling_dice:
                    dice_outcome = "("
                    dice_total = 0
                    roll_results = []
                    if (int(dice_rolled[0]) > dice_rolled_cap):
                        response = f"**{name}** is trying to roll to many dice.  Please try again with less"
                        rolling_dice = False
                        await context.reply(response)
                    elif (int(dice_rolled[1]) > die_size_cap): 
                        response = f"**{name}** is trying to roll to large of dice.  Please try again with smaller dice"
                        rolling_dice = False
                        await context.reply(response)
                    else:
                        for i in range(int(dice_rolled[0])):
                            roll_results.append(randint(1,int(dice_rolled[1])))

                        for i in range(len(roll_results)):
                            if (i == (int(dice_rolled[0])-1)):
                                if (roll_results[i] == int(dice_rolled[1])):
                                    dice_outcome += f"{ansi_green}{roll_results[i]}{ansi_clear})"
                                elif (roll_results[i] == 1):
                                    dice_outcome += f"{ansi_red}{roll_results[i]}{ansi_clear})"
                                else:
                                    dice_outcome += f"{ansi_blue}{roll_results[i]}{ansi_clear})"
                            else:
                                if (roll_results[i] == int(dice_size)):
                                    dice_outcome += f"{ansi_green}{roll_results[i]}{ansi_clear}, "
                                elif (roll_results[i] == 1):
                                    dice_outcome += f"{ansi_red}{roll_results[i]}{ansi_clear}, "
                                else:
                                    dice_outcome += f"{ansi_blue}{roll_results[i]}{ansi_clear}, "

                            dice_total += roll_results[i]

                        all_roll_formula.append(this_roll)
                        all_roll_results.append(dice_outcome)
                        all_roll_totals.append(dice_total)

            if rolling_dice:
                rolled_request = temp_request.format(*all_roll_totals)
                is_math = False
                logger.info(f"request split: {list(rolled_request)}")
                for i in list(rolled_request):
                    logger.info(f"Math Check loop: {i}")
                    if i in ['+','-','*','%','.','/']:
                        
                        is_math = True
                        break
                response = f"**{name}** is rolling {roll_request}\n```ansi\n"
                for i in range(len(all_roll_results)):
                    response += f"{all_roll_formula[i]} | {all_roll_results[i]} = {ansi_blue}{all_roll_totals[i]}{ansi_clear}\n"

                if is_math:
                    total = eval(rolled_request)
                    response += f"Total: {ansi_blue}{total}{ansi_clear}\n```"
                else:
                    response += f"\n```"

                await context.reply(response)

async def setup(bot) -> None:
    await bot.add_cog(DiceRoller(bot))