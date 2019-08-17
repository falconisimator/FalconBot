import discord
from discord.ext import commands
import todoist
import datetime

global path
path = "/falconshare/FalconBot/"

class TodoistCog:
    def __init__(self, bot):
        self.bot = bot

    global debuglv
    debuglv = 0

    @commands.command(name='todoist',
                description="runs some API tests on todoist",
                brief="Tests todoist API",
                aliases=['todo'])
    @commands.guild_only()
    async def todoist_test(self,ctx):
        APIkey = open(path+"Keys/todoist.txt", 'r').read().strip()
        try:
            api = todoist.TodoistAPI(APIkey)
            api.sync()
            full_name = api.state['user']['full_name']
            await ctx.send(full_name)
            for project in api.state['projects']:
                await ctx.send(project['name'])
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

        

# The setup function below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(TodoistCog(bot))

