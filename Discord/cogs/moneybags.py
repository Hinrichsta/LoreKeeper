import discord
import asyncio
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
        approve_reaction = '✅'
        deny_reaction = '❌'
        info = arg.split(',')
        response = ''
        pp = ''
        gp = ''
        sp = ''
        cp = ''
        owner = ''
        notes = ''
        indiv_trans = False
        trans_owner = False
        if ctx.author.display_name.split(' ')[1].strip('()') == "DM":
            #response = "The DM doesn't get to call Transactions!"
            #await ctx.send(response)
            pass
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
                elif i.casefold() in (name.casefold() for name in active_party):
                    owner = i.strip().capitalize()
                    indiv_trans = True
                    trans_owner = True
                elif "party" == i.casefold():
                    owner = i.strip().capitalize()
                    trans_owner = True
                else:
                    notes = i.strip()
            if not trans_owner:
                owner = ctx.author.display_name.split(' ')[1].strip('()')
            if pp == '':
                pp = '0'
            if gp == '':
                gp = '0'
            if sp == '':
                sp = '0'
            if cp == '':
                cp = '0'
            response = f"The following transaction will need to be Approved ({approve_reaction}) or Denied ({deny_reaction})```| Owner | PP | GP | SP | CP | Description |\n| {owner} | {pp} | {gp} | {sp} | {cp} | {notes} |```"

            def react_check(reaction, user):
                return user == ctx.message.author and str(reaction.emoji) in [approve_reaction, deny_reaction]

            msg = await ctx.send(response)
            await msg.add_reaction(approve_reaction)
            await msg.add_reaction(deny_reaction)

            try:
                reaction = await self.LoreKeeper_bot.wait_for("reaction_add", timeout=60.0 ,check=react_check)
            except asyncio.TimeoutError:
                    await ctx.send(content="Request Timeout: Transaction cancelled")
                    await msg.clear_reactions()
            else:
                if str(reaction[0]) == approve_reaction:
                    response_edit = f"The following transaction will be made```| Owner | PP | GP | SP | CP | Description |\n| {owner} | {pp} | {gp} | {sp} | {cp} | {notes} |```"
                    await msg.edit(content=response_edit)
                    await msg.clear_reactions()

                    trans_rep = set_ar_transaction(notes, pp, gp, sp, cp, owner)

                    if indiv_trans:
                        indiv_funds = get_individual_fund(owner)

                        new_response = f"Transaction Successful, ID: {trans_rep[0]}\nCurrent Individual Funds:```| {indiv_funds[0]} | {indiv_funds[1]}```"
                    else:
                        party_funds = get_party_funds()
                        indiv_funds = get_all_individual_funds()

                        new_response = f"Transaction Successful, ID: {trans_rep[0]}\nCurrent Party Funds:```{party_funds}```\nCurrent Individual Funds:```"
                        for ind in indiv_funds:
                            new_response += f"| {ind[0]} | {ind[1]} |\n"
                        new_response += "```"

                    await ctx.send(new_response)
                else: 
                    response_edit = "Transaction cancelled"
                    await msg.edit(content=response_edit)
                    await msg.clear_reactions()


    @commands.command()
    async def withdraw(self, ctx, *, arg):
        approve_reaction = '✅'
        deny_reaction = '❌'
        info = arg.split(',')
        response = ''
        pp = ''
        gp = ''
        sp = ''
        cp = ''
        owner = ''
        notes = ''
        indiv_trans = False
        trans_owner = False

        if ctx.author.display_name.split(' ')[1].strip('()') == "DM":
            #response = "The DM doesn't get to call Transactions!"
            #await ctx.send(response)
            pass
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
                elif i.casefold() in (name.casefold() for name in active_party):
                    owner = i.strip().capitalize()
                    indiv_trans = True
                    trans_owner = True
                elif "party" == i.casefold():
                    owner = i.strip().capitalize()
                    trans_owner = True
            if not trans_owner:
                owner = ctx.author.display_name.split(' ')[1].strip('()')
                indiv_trans = True
            if indiv_trans:
                before_funds = get_individual_fund(owner)[1]
            else:
                before_funds = get_party_funds()
            notes = info[len(info)-2]
            payee = info[len(info)-1]

            if pp == '':
                pp = '0'
            if gp == '':
                gp = '0'
            if sp == '':
                sp = '0'
            if cp == '':
                cp = '0'

            total_withdraw = (int(pp) * 10) + (int(gp)) + (int(sp) / 10) + (int(cp) / 100)

            if total_withdraw > before_funds:
                response = f"There are not enough funds to cover this transaction\nRequested Transaction:```| Owner | PP | GP | SP | CP | Description | Payee |\n| {owner} | {pp} | {gp} | {sp} | {cp} | {notes} | {payee} |```\nTotal Funds:``` {before_funds} ```"
                await ctx.send(response)
            else:
                response = f"The following transaction will need to be Approved ({approve_reaction}) or Denied ({deny_reaction})```| Owner | PP | GP | SP | CP | Description | Payee |\n| {owner} | {pp} | {gp} | {sp} | {cp} | {notes} | {payee} |```"

                def react_check(reaction, user):
                    return user == ctx.message.author and str(reaction.emoji) in [approve_reaction, deny_reaction]

                msg = await ctx.send(response)
                await msg.add_reaction(approve_reaction)
                await msg.add_reaction(deny_reaction)

                try:
                    reaction = await self.LoreKeeper_bot.wait_for("reaction_add", timeout=60.0 ,check=react_check)
                except asyncio.TimeoutError:
                        await ctx.send(content="Request Timeout: Transaction cancelled")
                        await msg.clear_reactions()
                else:
                    if str(reaction[0]) == approve_reaction:
                        response_edit = f"The following transaction will be made```| Owner | PP | GP | SP | CP | Description |\n| {owner} | {pp} | {gp} | {sp} | {cp} | {notes} |```"
                        await msg.edit(content=response_edit)
                        await msg.clear_reactions()

                        trans_rep = set_ap_transaction(notes, pp, gp, sp, cp, owner, payee)

                        if indiv_trans:
                            indiv_funds = get_individual_fund(owner)

                            new_response = f"Transaction Successful, ID: {trans_rep[0]}\nCurrent Individual Funds:```| {indiv_funds[0]} | {indiv_funds[1]}```"
                        else:
                            party_funds = get_party_funds()
                            indiv_funds = get_all_individual_funds()

                            new_response = f"Transaction Successful, ID: {trans_rep[0]}\nCurrent Party Funds:```{party_funds}```\nCurrent Individual Funds:```"
                            for ind in indiv_funds:
                                new_response += f"| {ind[0]} | {ind[1]} |\n"
                            new_response += "```"

                        await ctx.send(new_response)
                    else: 
                        response_edit = "Transaction cancelled"
                        await msg.edit(content=response_edit)
                        await msg.clear_reactions()
    
    @commands.command()
    async def date(self, ctx,):
        eth_date = get_etharus_date()
        response = f"The Date in Etharus is currently ```{eth_date[0]} {eth_date[1]}, {eth_date[2]}{eth_date[3]}```"
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
    async def allfunds(self, ctx):
        msg = await ctx.send("Gathering Data")
        party_funds = get_party_funds()
        indiv_funds = get_all_individual_funds()
        response = f"Current Party Funds:```{party_funds}```"
        response += f"\nCurrent Individual Funds:```"
        for ind in indiv_funds:
            response += f"| {ind[0]} | {ind[1]} |\n"
        response += "```"

        await msg.edit(content=response)
    
    @commands.command()
    async def partyfund(self, ctx):
        party_funds = get_party_funds()
        response = f"Current Party Funds:```{party_funds}```"

        await ctx.send(response)
    
    @commands.command()
    async def allindividual(self, ctx):
        msg = await ctx.send("Gathering Data")

        indiv_funds = get_all_individual_funds()
        response = "Current Individual Funds:```"
        for ind in indiv_funds:
            response += f"| {ind[0]} | {ind[1]} |\n"
        response += "```"

        await msg.edit(content=response)

    @commands.command()
    async def myfunds(self, ctx):
        member = ctx.author.display_name.split(' ')[1].strip('()')
        if(member == 'DM'):
            response = "Whatever you want it to be, you are the DM!"
        else:
            indiv_fund = get_individual_fund(member)
            response = f"Current individual fund for {member}```{indiv_fund[1]}```"

        await ctx.send(response)

    @commands.command()
    async def myitems(self, ctx):
        member = ctx.author.display_name.split(' ')[1].strip('()')
        if(member == 'DM'):
            response = "You already have all the items, give us more"
        else:
            mem_items = get_individual_magic_items(member)
        response = f"Items {member} currently has:\n"
        for mi in mem_items:
            response += f"* {mi[3]}\n * <{mi[7]}>\n"

        await ctx.send(response)

    @commands.command()
    async def storeditems(self, ctx):
        magic_items,item_owner = get_magic_items()
        response = "Magic Items currently in the Party Storage:\n"

        i = 0
        for mi in magic_items:
            if item_owner[i][0] == 'Party Stash' and (mi[8] == 'Active' or mi[8] == 'Storage'):
                response += f"* {mi[3]}\n * <{mi[7]}>\n"
            i += 1
            if len(response) >= 1900:
                await ctx.send(response)
                response = ''
        
        await ctx.send(response)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong")

    @commands.command()
    async def test(self, ctx):
        member = ctx.author.display_name.split(' ')[1].strip('()')

        await ctx.send(member)

    @commands.command()
    async def help(self, ctx):
        response = "``` LoreKeeper and Money Laundering Bot\n\nCommands: "
        response +="\n/deposit:    Deposit money into party or individual fund | Format: Owner, 0pp, 0gp, 0sp, 0cp, notes (Order does not matter. Owner may be ommited if withdrawing from individual fund.  You do not need to put all denominations but they need to have the denomination after the number)"
        response +="\n/withdraw:    Withdraw money from party or individual fund | Format: Owner, 0pp, 0gp, 0sp, 0cp, notes, payee (Structure at will but leave notes, and payee at the end.  Owner may be ommited if withdrawing from individual fund. You do not need to put all denominations but they need to have the denomination after the number)"
        response +="\n/date:    Shows the current date in Etharus"
        response +="\n/setdate:    Allows you to set the date in Etharus | Format: Season day,year (example Spring, 21, 1805AG Era may be omitted)"
        response +="\n/allfunds:    Shows the party fund and all the individual funds"
        response +="\n/partyfund:    Shows the current party fund amount"
        response +="\n/allindividual:    Shows all of the current individual funds"
        response +="\n/myfunds:    Shows the requestor's current individual funds"
        response +="\n/myitems:    Shows the requestor's currently held items"
        response +="\n/storeditems:    Shows the items currently in the party storage"
        response +="```"

        await ctx.send(response)

def setup(LoreKeeper_bot: commands.Bot):
    LoreKeeper_bot.add_cog(MoneyBags(LoreKeeper_bot))