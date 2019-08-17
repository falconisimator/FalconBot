#commitments.py 

import discord
from discord.ext import commands
import logging
import os
import time
import datetime
import traceback
import csv



class CommitmentCog:

    def __init__(self, bot):
        self.bot = bot

    global debuglv
    debuglv = 0
    
    global datapath
    datapath = '/falconshare/FalconBot/data/'

    @commands.command()
    @commands.guild_only()
    async def commit(self, ctx):
        try:
            commitment = ctx.message.content.split(' ', 1)[1]
            global datapath
            commits = open(datapath+"commitments.txt",'r+')
            commits.seek(0)
            if str(ctx.author) in commits.read():
                await ctx.send("You already have a commitment, maybe you should do that first?")
                commits.seek(0)
                await ctx.send("```"+commits.read()+"```")   
            else:
                commits.write(str(ctx.author)+": " + commitment + '\r\n') 
                commits.seek(0)
                await ctx.send("```"+commits.read()+"```")   
            commits.close()
        except Exception as e:
            logging.ERROR('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e)+'\r\n')
            await ctx.send('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e))

    @commands.command()
    @commands.guild_only()
    async def finished(self, ctx):
        try:
            global datapath
            commits = open(datapath+"commitments.txt",'r+')
            d = commits.readlines()
            commits.seek(0)
            for i in d:
                if str(ctx.author) not in i:
                    commits.write(i)
            commits.truncate()
            commits.close()
            await ctx.send("Commitment cleared. Congrats!")
        except Exception as e:
            logging.ERROR('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e)+'\r\n')
            await ctx.send('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e))

    @commands.command(aliases = ['comms','commits'])
    @commands.guild_only()
    async def commitments(self, ctx):
        try:
            global datapath
            commits = open(datapath+"commitments.txt",'r')
            commits.seek(0)
            if len(str(commits.read()))>0:
                commits.seek(0)
                await ctx.send("```"+commits.read()+"```")
                print(commits.read())
            else:
                await ctx.send("No commintments are posted.")
            commits.close()
        except Exception as e:
            logging.ERROR('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e)+'\r\n')
            await ctx.send('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e))
            
            
            
    
    async def log_error(self,ctx,e):
        global debuglv
        try:
            if debuglv >0:
                await ctx.send(traceback.format_exc())
            now = datetime.datetime.now()
            print('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e))
            await ctx.send('**`ERROR:`**'+ str(type(e).__name__) +' - '+ str(e))
            logging.ERROR(str(now) + ': '+ str(type(e).__name__) +' - '+ str(e)+'.\r\n')
        except Exception as e:
            await ctx.send('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e))


def setup(bot):
    bot.add_cog(CommitmentCog(bot))
