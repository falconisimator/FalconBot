import discord
from discord.ext import commands
import logging
import os
import time
import datetime
import traceback


class OwnerCog:

    def __init__(self, bot):
        self.bot = bot

    global debuglv
    debuglv = 0
    
    # Hidden means it won't show up on the default help.
    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def cog_load(self, ctx, *, cog: str):
        """Command which Loads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await self.log_error(ctx,e)
        else:
            await ctx.send('**`SUCCESS`**')


    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def cog_unload(self, ctx, *, cog: str):
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await self.log_error(ctx,e)
        else:
            await ctx.send('**`SUCCESS`**')


    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def cog_reload(self, ctx, *, cog: str):
        """Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await self.log_error(ctx,e)
        else:
            await ctx.send('**`SUCCESS`**')


    @commands.command(name='restart', hidden=True)
    @commands.is_owner()
    async def bot_restart(self, ctx):
        try:
            await ctx.send("Restarting...")
            os.system("python3 /falconshare/FalconBot/FalconBotv2.py")
            time.sleep(0.5) # 200ms to CTR+C twice
            quit()
        except Exception as e:
            await self.log_error(ctx,e)
        else:
            await ctx.send('**`SUCCESS`**')


    @commands.command(name='log', hidden=True)
    @commands.is_owner()
    async def print_log(self, ctx):
        try:
            await ctx.send("Fetching Log File")
            await ctx.send(file=discord.File('/falconshare/FalconBot/log.txt'))
        except Exception as e:
            await self.log_error(ctx,e)

    @commands.command(name='debug', hidden=True)
    @commands.is_owner()
    async def debuglevel(self, ctx,*level):
        global debuglv
        try:
            debuglv=int(level[0])
            ctx.send('debug level set to: '+str(debuglv))
        except Exception as e:
            await self.log_error(ctx,e)


    @commands.command(name='testlog', hidden=True)
    @commands.is_owner()
    async def test_log(self, ctx):
        try:
            now = datetime.datetime.now()
            await ctx.send(str(now)+": Printing to log file")
            logging.info(str(now)+': Test text for log file \r\nA New line for log file\r\n')
            await ctx.send(file=discord.File('/falconshare/FalconBot/log.txt'))
        except Exception as e:
            await self.log_error(ctx,e)
            
    
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
    
    # @commands.command(pass_context = True)
    # async def clear(context, number):

    #     users = ['Falcon#6280']
    #     servers = ['r/EScapees','ControlEngineering']
    #     channels = ['lobby']
    #     protected = ['515882602528374803']

    #     if str(context.message.author) in users and str(context.message.server) in servers and str(context.message.channel) in channels:
    #         mgs = [] #Empty list to put all the messages in the log
    #         number = int(number) #Converting the amount of messages to delete to an integer
    #         async for x in client.logs_from(context.message.channel, limit = number):
    #             if x.id not in protected:
    #                 mgs.append(x)
    #             else:
    #                 print(x.id + ' is Protected')
    #         await client.delete_messages(mgs)
    #         #await client.say(mgs)
    #     else:
    #         await client.say("You do not have permissions for this dangerous feature here")
    #         print(context.message.author)


def setup(bot):
    bot.add_cog(OwnerCog(bot))
