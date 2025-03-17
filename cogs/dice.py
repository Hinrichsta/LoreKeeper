import random
import re

import discord
import logging
from random import randint
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

logger = logging.getLogger("discord_bot")

# ANSI Color Codes
ansi_blue = "\u001b[0;34m"
ansi_green = "\u001b[0;32m"
ansi_red = "\u001b[0;31m"
ansi_light_grey = "\u001b[0;30m"
ansi_clear = "\u001b[0;0m"



class DiceRoller(commands.Cog, name="Dice Roller"):
    def __init__(self, bot) -> None:
        self.bot = bot


    @commands.hybrid_command(name="roll", aliases=["r"], description="List all commands the bot has loaded.")
    async def roll(self, context: Context, roll_request: str) -> None:
        """
        Roll the dice and see what you get.

        :param context: The hybrid command context.
        :param roll: The formula for the requested roll.
        """
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
            name = context.author.display_name.split(' ')[1].strip('()')
        else:
            name = context.author.display_name
        
        # Other Variables
        dice_rolled_cap = 500
        die_size_cap = 1000

        parsed_roll_requests = re.findall(pattern_all, roll_request)
        temp_request = re.sub(pattern_all, "#", roll_request)
        all_roll_formula = []
        all_roll_results = []
        all_roll_totals = []

        # start Logger
        logger.info(f"Rolling some dice for {context.author.display_name}.  Requested Roll: {roll_request}")

        for r in parsed_roll_requests:
            # Looks for requests using Advantage
            if re.match(pattern_adv, r):
                this_roll = r.lower()
                dice_rolled = this_roll.split("d")
                dice_size = (dice_rolled[1].split('kh'))[0]
                dice_outcome = "("
                dice_total = 0
                roll_results = []
                roll_adv = []

                if (int(dice_rolled[0]) > dice_rolled_cap):
                    response = f"**{name}** is trying to roll to many dice.  Please try again with less"
                    await context.reply(response)
                elif (int(dice_size) > die_size_cap): 
                    response = f"**{name}** is trying to roll to large of dice.  Please try again with smaller dice"
                    await context.reply(response)
                else:
                    #Runs through the dice rolled, and puts them into a list
                    for i in range(int(dice_rolled[0])):
                        roll_results.append(randint(1,int(dice_size)))
                    
                    #Advantage Checks.  Will look to see if it is straight advantage, or if is a count of advantage
                    if re.fullmatch(pattern_adv_plus, this_roll):
                        temp_list = roll_results
                        needed_die = int((dice_rolled[1].split('kh'))[1])

                        for i in range(needed_die):
                            highest = 0
                            for j in range(len(temp_list)):
                                if temp_list[j] > highest:
                                    highest = temp_list[j]
                            temp_list.remove(highest)
                            roll_adv.append(highest)
                        logger.info(f"{roll_adv}")
                    else:
                        roll_adv.append(max(roll_results))

                    j = 0 # Used to count how
                    for i in range(len(roll_results)):
                        if j < len(roll_adv): # Checks to see if the advantage has been found
                            done_check = False
                            for k in range(len(roll_adv)): #Runs through the advantage max, starting and the next number each time it is found
                                if roll_results[i] == roll_adv[k+j]: # Checks to see if the current result equals the highest value
                                    if (i == (int(dice_rolled[0])-1)):
                                        if (roll_results[i] == int(dice_size)):
                                            dice_outcome += f"{ansi_green}{roll_results[i]}{ansi_clear})"
                                        elif (roll_results[i] == 1):
                                            dice_outcome += f"{ansi_red}{roll_results[i]}{ansi_clear})"
                                        else:
                                            dice_outcome += f"{ansi_blue}{roll_results[i]}{ansi_clear})"
                                    else:
                                        if (roll_results[i] == 20):
                                            dice_outcome += f"{ansi_green}{roll_results[i]}{ansi_clear}, "
                                        elif (roll_results[i] == 1):
                                            dice_outcome += f"{ansi_red}{roll_results[i]}{ansi_clear}, "
                                        else:
                                            dice_outcome += f"{ansi_blue}{roll_results[i]}{ansi_clear}, "
                                    dice_total += roll_results[i]
                                    j += 1
                                    done_check = True
                            if not done_check:
                                dice_outcome += f"{ansi_light_grey}{roll_results[i]}{ansi_clear}, "
                        else:  
                            dice_outcome += f"{ansi_light_grey}{roll_results[i]}{ansi_clear}, "
                    
                    all_roll_formula.append(this_roll)
                    all_roll_results.append(dice_outcome)
                    all_roll_totals.append(dice_total)

            
            # Looks for roll requests using Disadvantage
            elif re.match(pattern_disadv, r):
                this_roll = r.lower()
                dice_rolled = this_roll.split("d")
                dice_size = (dice_rolled[1].split('kl'))[0]
                dice_outcome = "("
                dice_total = 0
                roll_results = []
                roll_disadv = []

                if (int(dice_rolled[0]) > dice_rolled_cap):
                    response = f"**{name}** is trying to roll to many dice.  Please try again with less"
                    await context.reply(response)
                elif (int(dice_size) > die_size_cap): 
                    response = f"**{name}** is trying to roll to large of dice.  Please try again with smaller dice"
                    await context.reply(response)
                else:
                    #Runs through the dice rolled, and puts them into a list
                    for i in range(int(dice_rolled[0])):
                        roll_results.append(randint(1,int(dice_size)))
                    
                    #Disddvantage Checks.  Will look to see if it is straight disadvantage, or if is a count of disadvantage
                    if re.fullmatch(pattern_disadv_plus, this_roll):
                        temp_list = roll_results
                        needed_die = int((dice_rolled[1].split('kl'))[1])

                        for i in range(needed_die):
                            lowest = dice_size
                            for j in range(len(temp_list)):
                                if temp_list[j] > lowest:
                                    lowest = temp_list[j]
                            temp_list.remove(lowest)
                            roll_disadv.append(lowest)
                    else:
                        roll_disadv.append(min(roll_results))

                    j = 0 # Used to count how
                    for i in range(len(roll_results)):
                        if j < len(roll_disadv): # Checks to see if the disadvantage has been found
                            done_check = False
                            for k in range(len(roll_disadv)): #Runs through the advantage min, starting and the next number each time it is found
                                if roll_results[i] == roll_disadv[k+j]: # Checks to see if the current result equals the lowest value
                                    if (i == (int(dice_rolled[0])-1)):
                                        if (roll_results[i] == int(dice_size)):
                                            dice_outcome += f"{ansi_green}{roll_results[i]}{ansi_clear})"
                                        elif (roll_results[i] == 1):
                                            dice_outcome += f"{ansi_red}{roll_results[i]}{ansi_clear})"
                                        else:
                                            dice_outcome += f"{ansi_blue}{roll_results[i]}{ansi_clear})"
                                    else:
                                        if (roll_results[i] == 20):
                                            dice_outcome += f"{ansi_green}{roll_results[i]}{ansi_clear}, "
                                        elif (roll_results[i] == 1):
                                            dice_outcome += f"{ansi_red}{roll_results[i]}{ansi_clear}, "
                                        else:
                                            dice_outcome += f"{ansi_blue}{roll_results[i]}{ansi_clear}, "
                                    dice_total += roll_results[i]
                                    j += 1
                                    done_check = True
                            if not done_check:
                                dice_outcome += f"{ansi_light_grey}{roll_results[i]}{ansi_clear}, "
                        else:  
                            dice_outcome += f"{ansi_light_grey}{roll_results[i]}{ansi_clear}, "

                    all_roll_formula.append(this_roll)
                    all_roll_results.append(dice_outcome)
                    all_roll_totals.append(dice_total)
                 
            # Looks for all standard roll requests
            else:
                this_roll = r.lower()
                dice_rolled = this_roll.split("d")
                dice_outcome = "("
                dice_total = 0
                roll_results = []

                if (int(dice_rolled[0]) > dice_rolled_cap):
                    response = f"**{name}** is trying to roll to many dice.  Please try again with less"
                    await context.reply(response)
                elif (int(dice_rolled[1]) > die_size_cap): 
                    response = f"**{name}** is trying to roll to large of dice.  Please try again with smaller dice"
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
                            if (roll_results[i] == 20):
                                dice_outcome += f"{ansi_green}{roll_results[i]}{ansi_clear}, "
                            elif (roll_results[i] == 1):
                                dice_outcome += f"{ansi_red}{roll_results[i]}{ansi_clear}, "
                            else:
                                dice_outcome += f"{ansi_blue}{roll_results[i]}{ansi_clear}, "

                        dice_total += roll_results[i]

                    all_roll_formula.append(this_roll)
                    all_roll_results.append(dice_outcome)
                    all_roll_totals.append(dice_total)


        response = f"**{name}** is rolling {roll_request}\n```ansi\n"
        for i in range(len(all_roll_results)):
            response += f"{all_roll_formula[i]} | {all_roll_results[i]} = {ansi_blue}{all_roll_totals[i]}{ansi_clear}\n```"

        #embed = discord.Embed(
        #    title=f"```ansi\nrolling {ansi_blue}{dice_rolled[0]}d{dice_rolled[1]}{ansi_clear}\n``",
        #    description=f"```ansi\n{dice_outcome} = {ansi_blue}{dice_total}{ansi_clear}\n```",
        #)

        await context.reply(response)




async def setup(bot) -> None:
    await bot.add_cog(DiceRoller(bot))