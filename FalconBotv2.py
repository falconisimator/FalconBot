import discord
from discord.ext import commands
import logging
import requests

import sys, traceback

global debuglv
debuglv = 0


def get_file_contents(filename):
    """ Given a filename,
        return the contents of that file
    """
    try:
        with open(filename, 'r') as f:
            # It's assumed our file contains a single line,
            # with our API key
            return f.read().strip()
    except FileNotFoundError:
        print("'%s' file not found" % filename)

TOKEN = get_file_contents("Keys/BotKey.txt")

all_extensions = [  'cogs.mathTools',
                    'cogs.members',
                    'cogs.owner',
                    'cogs.controlTools',
                    'cogs.dataTools',
                    'cogs.commitments',
                    'cogs.Weather']                    
try:
    logging.basicConfig( level=logging.INFO,handlers=[logging.FileHandler('/falconshare/FalconBot/log.txt', 'a','utf-8')])
except:
    logging.basicConfig( level=logging.INFO,handlers=[logging.FileHandler('/falconshare/FalconBot/log.txt', 'w','utf-8')])
    logging.ERROR('Append mode could not be used, log file refreshed.')



prefixes=['?','^']

def get_prefix(bot, message):
    if not message.guild:
        # Only allow ? to be used in DMs
        return '?'
    return commands.when_mentioned_or(*prefixes)(bot, message)


bot = commands.Bot(command_prefix=get_prefix, description='A Rewrite Cog Example')


# Below cogs represents our folder our cogs are in. Following is the file name. So 'meme.py' in cogs, would be cogs.meme
# Here we load our extensions(cogs) listed above in [initial_extensions].
if __name__ == '__main__':
    for extension in all_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            logging.warning('Failed to load extension '+str(extension)+':  '+ str(type(e).__name__) +' - '+ str(e)+'.\r\n')
            print('Failed to load extension '+str(extension)+':  '+ str(type(e).__name__) +' - '+ str(e)+'.\r\n')
            #traceback.print_exc()


@bot.event
async def on_ready():
    logging.info('\r\n-------------------------------------------------------------------\r\n')
    logging.info('Logged in as: '+str(bot.user.name)+ ' - ' +str(bot.user.id)+'\r\nVersion: '+str(discord.__version__)+'\r\n')
    activity = discord.Game(name="New and Improved?")
    await bot.change_presence(status=discord.Status.idle, activity=activity)
    logging.info('Successfully logged in and booted...!\r\n')

# @bot.event
# async def on_message(message):
#     print(str(message.author)+'@'+message.guild.name+' - '+message.channel.name+': '+message.content)
#     if message.content.lower().__contains__('hi bot'):
#         await message.channel.send('Hi '+message.author.display_name)
#     if message.content.lower().__contains__('hi erik'):
#         await message.channel.send("You meant 'Hi Eric'")
#     await bot.process_commands(message)



bot.run(TOKEN, bot=True, reconnect=True)
