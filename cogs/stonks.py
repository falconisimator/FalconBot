import discord
from discord.ext import commands
from tinydb import TinyDB, Query

global path
path = "/falconshare/FalconBot/"


class StonksCog:
    """StonksCog"""

    def __init__(self, bot):
        self.bot = bot

    global debuglv
    debuglv = 0

    global db 
    db = TinyDB(path+'stonks.json')
    
    @commands.command()
    @commands.guild_only()
    async def buy(self, ctx, amount, user):
        try:
            User = Query()
            Balance = db.search((User.type == 'account') & (User.user == str(ctx.author)))[0]['balance']
            if (float(Balance)<float(amount)) | (float(amount)<0):
                await ctx.send('Balance is insufficiant for your purchase.')
            else:
                Result = db.search((User.type=='record') & (User.user == str(ctx.message.mentions[0])))
                total=0
                n=0
                for item in Result:
                    total = total + int(item['length'])
                    n=n+1
                Price = max(float(len(Result))/500+(total/n)/10,1)
                Position = db.search((User.type == 'position') & (User.user == str(ctx.author)) & (User.stonk == str(ctx.message.mentions[0])))
                if len(Position)>0:
                    db.update({'units': float(Position[0]['units'])+float(amount)/Price},(User.type == 'position') & (User.user == str(ctx.author)) & (User.stonk == str(ctx.message.mentions[0])))
                    await ctx.send('You now have: ' + "{0:.2f}".format(float(Position[0]['units'])+float(amount)/Price) + ' units of '+str(ctx.message.mentions[0]))
                else:
                    db.insert({'units': float(amount)/Price,'type' : 'position' , 'user' : str(ctx.author) , 'stonk' : str(ctx.message.mentions[0])})
                    await ctx.send('You now have: ' + "{0:.2f}".format(float(amount)/Price) + ' units of '+str(ctx.message.mentions[0]))
                db.update({'balance':Balance-float(amount)},(User.type == 'account') & (User.user == str(ctx.author)))


        except Exception as e:
            log_error(e)

    @commands.command()
    @commands.guild_only()
    async def sell(self, ctx, amount, user):
        try:
            User = Query()
            Balance = db.search((User.type == 'account') & (User.user == str(ctx.author)))[0]['balance']
            Position = db.search((User.type == 'position') & (User.user == str(ctx.author)) & (User.stonk == str(ctx.message.mentions[0])))
            if (float(Position[0]['units'])<float(amount)) | (float(amount)<0):
                await ctx.send('You do not have that many units.')
            else:
                Result = db.search((User.type=='record') & (User.user == str(ctx.message.mentions[0])))
                total=0
                n=0
                for item in Result:
                    total = total + int(item['length'])
                    n=n+1
                Price = max(float(len(Result))/500+(total/n)/10,1)
                Position = db.search((User.type == 'position') & (User.user == str(ctx.author)) & (User.stonk == str(ctx.message.mentions[0])))
                db.update({'units': float(Position[0]['units'])-float(amount)},(User.type == 'position') & (User.user == str(ctx.author)) & (User.stonk == str(ctx.message.mentions[0])))
                db.update({'balance':Balance+float(amount)*Price},(User.type == 'account') & (User.user == str(ctx.author)))
                await ctx.send('You now have: ' + "{0:.2f}".format(float(Position[0]['units'])-float(amount)) + ' units of '+str(ctx.message.mentions[0])) + "\nBalance: " + str(Balance+float(amount)*Price) + "Credits"
        except Exception as e:
            log_error(e)

    @commands.command()
    @commands.guild_only()
    async def portfolio(self, ctx):
        try:
            User = Query()
            Positions = db.search((User.type == 'position') & (User.user == str(ctx.author)))
            String = "```Portfolio for: " + str(ctx.author) + "\n-----------------------------------------------------------\n"
            Balance = db.search((User.type == 'account') & (User.user == str(ctx.author)))[0]['balance']
            String=String + "Balance: " + str(Balance) +" Credits \n"
            Total_value = Balance
            for position in Positions:
                Result = db.search((User.type=='record') & (User.user == position['stonk']))
                total=0
                n=0
                for item in Result:
                    total = total + int(item['length'])
                    n=n+1
                Price = max(float(len(Result))/500+(total/n)/10,1)
                String=String + "Stonk: " + position['stonk'] + "  Units: " + "{0:.2f}".format(float(position['units'])) + "  Value: " + "{0:.2f}".format(float(position['units']*Price))+" Credits \n"
                Total_value = Total_value + position['units']*Price
            String=String +"-----------------------------------------------------------\n"+"Total value: " + "{0:.2f}".format(Total_value) + " credits```"
            await ctx.send(String)
        except Exception as e:
            log_error(e)

    @commands.command()
    @commands.guild_only()
    async def stonk(self, ctx, user):
        try:
            User = Query()
            Result = db.search((User.type=='record') & (User.user == str(ctx.message.mentions[0])))
            total=0
            n=0
            for item in Result:
                total = total + int(item['length'])
                n=n+1
            await ctx.send('Current unit price: '+"{0:.2f}".format(max(float(len(Result))/500+(total/n)/10,1))+' credits' )
        except Exception as e:
            log_error(e)

    @commands.command()
    @commands.guild_only()
    async def stonks(self, ctx):
        try:
            User = Query()
            String = "```"
            for member in ctx.guild.members:
                Result = db.search((User.type=='record')& (User.user == str(member)))
                if len(Result)>0:
                    total=0
                    n=0
                    for item in Result:
                        total = total + int(item['length'])
                        n=n+1
                    String = String + 'Unit price for '+ str(member) +" : {0:.2f}".format(max(float(len(Result))/500+(total/n)/10,1))+' credits\n' 
            String = String+"```"
            await ctx.send(String)
        except Exception as e:
            log_error(e)

    @commands.command()
    @commands.guild_only()
    async def balance(self, ctx):
        try:
            #await ctx.send(str(ctx.author))
            User = Query()
            Result = db.search((User.type == 'account') & (User.user == str(ctx.author)))
            if len(Result)==0:
                db.insert({'type':'account','user':str(ctx.author),'balance':1000})
                await ctx.send('Initial balance of 1000 credits created')
            else:
                #await ctx.send(Result[0])
                await ctx.send(str(Result[0]['balance'])+' Credits')
        except Exception as e:
            log_error(e)

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def purge(self, ctx):
        try:
            user = ctx.message.mentions[0]
            User = Query()
            db.remove((User.type == 'account') & (User.user == str(user)))
            db.remove((User.type == 'position') & (User.user == str(user)))
            await ctx.send("User " + str(user) + " purged.")
        except Exception as e:
            log_error(e)

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def stats(self, ctx):
        try:
            User = Query()
            Result = db.search((User.type=='record') & (User.user == str(ctx.message.mentions[0])))
            total=0
            n=0
            for item in Result:
                total = total + int(item['length'])
                n=n+1
            await ctx.send(str(len(Result))+' '+str(total)+' '+str(n)+ ' ' + str(total/n))
        except Exception as e:
            log_error(e)


    async def on_message(self,message):
        db.insert({'type':'record','user':str(message.author),'guild':str(message.guild),'timestamp':str(message.created_at), 'length':len(message.content)})

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
    bot.add_cog(StonksCog(bot))