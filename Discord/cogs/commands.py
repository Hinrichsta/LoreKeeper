import discord
from discord.ext import commands
from Database.Database import Lore_Session
from Database.Parse import *
from Database.Input import *


active_party_all = get_active_party()
active_party = []
for apa in active_party_all:
    active_party.append(apa[1])

class MoneyBags(commands.Cog):
    def __init__(self, LoreKeeper_bot):
        self.LoreKeeper_bot = LoreKeeper_bot

    @commands.command()
    async def deposit(self, ctx, *, arg):
        info = arg.split(',')
        response = ''
        pp = ''
        gp = ''
        sp = ''
        cp = ''
        owner = ''
        notes = ''

        if len(info) > 6:
            response = "To Many Arguments"
        elif len(info) < 3:
            response = "Not Enough Arguments"
        else:
            for i in info:
                i.strip()
                if "pp" in i.casefold():
                    pp = i.strip('pp')
                elif "gp" in i.casefold():
                    gp = i.strip('gp')
                elif "sp" in i.casefold():
                    gp = i.strip('sp')
                elif "cp" in i.casefold():
                    gp = i.strip('cp')
                elif i.casefold() in (name.casefold() for name in active_party) or "party" == i.casefold():
                    if "party" in i.casefold():
                        owner = "The Party"
                    else:
                        owner = i.strip()
                else:
                    notes = i.strip()
            if pp == '':
                pp = '0'
            if gp == '':
                gp = '0'
            if sp == '':
                sp = '0'
            if cp == '':
                cp = '0'

            response = f"**{owner}** is depositing **{pp}** Platinum, **{gp}** Gold, {sp} Silver, {cp} Copper into the Party Fund Because {notes}"


        await ctx.send(response)

    @commands.command()
    async def withdraw(self, ctx, *, arg):
        return NotImplementedError
    
    @commands.command()
    async def date(self, ctx,):
        eth_date = get_etharus_date()
        response = f"The Date in Etharus is currently ```{eth_date}```"
        await ctx.send(response)

    @commands.command()
    async def setdate(self, ctx, *, arg):
        season = arg.split(' ', 1)[0].strip(' ')
        later = arg.split(' ', 1)[1]
        day = later.split(',', 1)[0].strip(' ')
        year = later.split(',', 1)[1].strip(' ')
        if 'AG' in year:
            year = year.strip('AG')

        result = set_etharus_date(season,day,year)

        if result == "Error: Season":
            response = f"Date could not be set due to incorrect season ```{season}```"
        elif result == "Error: Date":
            response = f"Date could not be set due to incorrect day ```{day}```"
        else:
            eth_date = get_etharus_date()
            response = f"The Date in Etharus is currently ```{eth_date}```"
            
        await ctx.send(response)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong")

    @commands.command()
    async def test(self, ctx, args):
        await ctx.send(args)

def setup(LoreKeeper_bot: commands.Bot):
    LoreKeeper_bot.add_cog(MoneyBags(LoreKeeper_bot))