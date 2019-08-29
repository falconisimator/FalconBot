import discord
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from discord.ext import commands
from tinydb import TinyDB, Query
import sys

global path
path = "/falconshare/FalconBot/"
sys.path.append(path)

from PricingModule import Pricing, Pricing_lst


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
                if len(ctx.message.mentions)==0:
                    user = user
                else:
                    user = str(ctx.message.mentions[0])
                if user == str(ctx.author):                
                    await ctx.send("You may not buy yourself this isn't some auto-metalacio.")
                else:
                    Price = Pricing(user,db)
                    Position = db.search((User.type == 'position') & (User.user == str(ctx.author)) & (User.stonk == user))
                    if len(Position)>0:
                        db.update({'units': float(Position[0]['units'])+float(amount)/Price},(User.type == 'position') & (User.user == str(ctx.author)) & (User.stonk == user))
                        if Position[0]['buy_price']:
                            db.update({'buy_price': float(Position[0]['buy_price'])+float(amount)},(User.type == 'position') & (User.user == str(ctx.author)) & (User.stonk == user))
                        else:
                            db.update({'buy_price': amount},(User.type == 'position') & (User.user == str(ctx.author)) & (User.stonk == user))
                        await ctx.send('You now have: ' + "{0:.2f}".format(float(amount)/Price) + ' new units of '+ user +"for a total of: {0:.2f}".format(float(Position[0]['units'])+float(amount)/Price) + ' units')
                    else:
                        db.insert({'units': float(amount)/Price,'type' : 'position' , 'user' : str(ctx.author) , 'stonk' : user, 'buy_price': amount})
                        await ctx.send('You now have: ' + "{0:.2f}".format(float(amount)/Price) + ' units of '+ user)
                    db.update({'balance':Balance-float(amount)},(User.type == 'account') & (User.user == str(ctx.author)))


        except Exception as e:
            log_error(e)

    @commands.command()
    @commands.guild_only()
    async def sell(self, ctx, amount, user):
        try:
            User = Query()
            if len(ctx.message.mentions)==0:
                0==0
            else:
                user = str(ctx.message.mentions[0])
            Balance = db.search((User.type == 'account') & (User.user == str(ctx.author)))[0]['balance']
            Position = db.search((User.type == 'position') & (User.user == str(ctx.author)) & (User.stonk == user))
            if amount == 'all':
                Price = Pricing(user,db)
                amount = Position[0]['units']
                db.remove((User.type == 'position') & (User.user == str(ctx.author)) & (User.stonk == user))
                db.update({'balance':Balance+float(amount)*Price},(User.type == 'account') & (User.user == str(ctx.author)))
                await ctx.send('You now have: ' + "{0:.2f}".format(float(Position[0]['units'])-float(amount)) + ' units of '+ user  + "\nBalance: " + "{0:.2f}".format(Balance+float(amount)*Price) + "Credits")
            elif (float(Position[0]['units'])<float(amount)) | (float(amount)<0):
                await ctx.send('You do not have that many units.')
            else:
                Price = Pricing(user,db)
                Position = db.search((User.type == 'position') & (User.user == str(ctx.author)) & (User.stonk == user))
                db.update({'buy_price': float(Position[0]['buy_price'])*((float(Position[0]['units'])-float(amount))/float(Position[0]['units'])) },(User.type == 'position') & (User.user == str(ctx.author)) & (User.stonk == user))
                db.update({'units': float(Position[0]['units'])-float(amount)},(User.type == 'position') & (User.user == str(ctx.author)) & (User.stonk == user))
                db.update({'balance':Balance+float(amount)*Price},(User.type == 'account') & (User.user == str(ctx.author)))
                await ctx.send('You now have: ' + "{0:.2f}".format(float(Position[0]['units'])-float(amount)) + ' units of '+user) + "\nBalance: " + str(Balance+float(amount)*Price) + " Credits"
        except Exception as e:
            log_error(e)

    @commands.command()
    @commands.guild_only()
    async def portfolio(self, ctx):
        try:
            User = Query()
            Positions = db.search((User.type == 'position') & (User.user == str(ctx.author)))
            String = "```Portfolio for: " + str(ctx.author) + "\n----------------------------------------------------------------------------------------------------------------------\n"
            Balance = db.search((User.type == 'account') & (User.user == str(ctx.author)))[0]['balance']
            String=String + "Balance: " + str(Balance) +" Credits \n"
            Total_value = Balance
            for position in Positions:
                Price = Pricing(position['stonk'],db)
                Value = float(position['units']*Price)
                String=String + "Stonk: " + position['stonk'].ljust(22, " ") + "  Units: " + ("{0:.2f}".format(float(position['units']))).rjust(8, " ") + "  Value: " + ("{0:.2f}".format(Value)).rjust(8, " ")+" Credits" + "  Bought for: " + "{0:.2f}".format(float(position['buy_price'])).rjust(8, " ")+" Credits  P/L:" + "{0:.2f}".format(100*(Value-float(position['buy_price']))/float(position['buy_price'])).rjust(8, " ")+"%"+"\n"
                #String=String + "Stonk: " + position['stonk'].ljust(22, " ") + "  Units: " + ("{0:.2f}".format(float(position['units']))).rjust(8, " ") + "  Value: " + ("{0:.2f}".format(float(position['units']*Price))).rjust(8, " ")+" Credits\n"
                Total_value = Total_value + position['units']*Price
            String=String +"----------------------------------------------------------------------------------------------------------------------\n"+"Total value: " + "{0:.2f}".format(Total_value) + " credits```"
            await ctx.send(String)
        except Exception as e:
            log_error(e)

    @commands.command()
    @commands.guild_only()
    async def stonk(self, ctx, user):
        try:
            User = Query()
            if len(ctx.message.mentions)==0:
                Result = db.search((User.type=='record') & (User.user == user))
            else:
                Result = db.search((User.type=='record') & (User.user == str(ctx.message.mentions[0])))
                user = str(ctx.message.mentions[0])
            Ordered = (sorted(Result, key=lambda k: k['timestamp'], reverse = False))
            History_X = []
            History_Y = []
            for i in range(5,max(len(Ordered)-1,5)):
                Price = Pricing_lst(Ordered[0:i],db)
                History_X.append(mdates.date2num(datetime.datetime.strptime(Ordered[i]['timestamp'].split(".")[0], '%Y-%m-%d %H:%M:%S')))
                History_Y.append(Price)
            plt.plot(History_X, History_Y,linestyle='-')
            plt.gcf().autofmt_xdate()
            myFmt = mdates.DateFormatter('%m-%d %H:%M')
            plt.gca().xaxis.set_major_formatter(myFmt)
            plt.title('Price history for '+ user )
            plt.xlabel('Date')
            plt.ylabel('Price (Credits)')
            plt.savefig(path+'/Stonk.png')
            plt.clf()
            await ctx.send(file=discord.File(path+"/Stonk.png"))
            await ctx.send('Current unit price: '+"{0:.2f}".format(Pricing(user,db))+' credits' )
        except Exception as e:
            log_error(e)

    @commands.command()
    @commands.guild_only()
    async def stonks(self, ctx):
        try:
            User = Query()
            String = "```"
            temp_list = []
            for member in ctx.guild.members:
                Result = db.search((User.type=='record')& (User.user == str(member)))
                if len(Result)>0:
                    temp_list.append((str(member),Pricing(str(member),db)))
                    
            temp_list = sorted(temp_list, key=lambda x:x[1],reverse=True)

            for element in temp_list:
                 String = String + 'Unit price for '+ element[0].ljust(22, " ") +" : "+("{0:.2f}".format(element[1])).rjust(6," ")+' credits\n' 
            String = String+"```"
            await ctx.send(String)
        except Exception as e:
            log_error(e)

    @commands.command()
    @commands.guild_only()
    async def Leaderboard(self, ctx):
        try:
            User = Query()
            String = "```"
            temp_list = []
            for member in ctx.guild.members:
                Positions = db.search((User.type == 'position') & (User.user == str(member)))
                Balance = db.search((User.type == 'account') & (User.user == str(member)))
                if len(Balance)>0:
                    Balance = Balance[0]['balance']
                if len(Positions)>0:
                    Total_value = Balance
                    for position in Positions:
                        Price = Pricing(position['stonk'],db)
                        Value = float(position['units']*Price)
                        Total_value = Total_value + position['units']*Price
                    temp_list.append((str(member),Total_value))        
            temp_list = sorted(temp_list, key=lambda x:x[1],reverse=True)
            n = 0
            for element in temp_list:
                 String = String + 'Total value of '+ element[0].ljust(22, " ") +" : "+("{0:.2f}".format(element[1])).rjust(10," ")+' credits\n' 
                 n=n+1
                 if n>10:
                    break
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

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def update_DB(self, ctx):
        try:
            User = Query()
            Positions = db.search((User.type == 'position'))
            n=0
            for position in Positions:
                try: 
                    position['buy_price']
                except:
                    db.update({'buy_price': float(position['units'])*Pricing(position['user'])},(User.type == 'position') & (User.user == position['user']) & (User.stonk == position['stonk']))
                    n = n+1
            ctx.send(str(n) + " fields were updated")
        except Exception as e:
            log_error(e)

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def test(self, ctx, user):
        try:
            User = Query()
            Result = db.search((User.type=='record') & (User.user == str(ctx.message.mentions[0])))
            Ordered = (sorted(Result, key=lambda k: k['timestamp'], reverse = False))
            History_X = []
            History_Y = []
            for i in range(1,max(len(Ordered)-1,5)):
                Price = Pricing_lst(Ordered[0:i])
                History_X.append(mpd.date2num(datetime.datetime.strptime(Ordered[i]['timestamp'], '%Y-%m-%d %H:%M:%S.%f')))
                History_Y.append(Price)
            plt.plot(History_X, History_Y,linestyle='-')
            plt.gcf().autofmt_xdate()
            plt.xlabel('Date')
            plt.ylabel('Price (Credits)')
            plt.savefig(path+'/Stonk.png')
            plt.clf()
            await ctx.send(file=discord.File(path+"/Stonk.png"))
            await ctx.send('Current unit price: '+"{0:.2f}".format(Pricing(str(ctx.message.mentions[0])))+' credits' )
        except Exception as e:
            log_error(e)

    @commands.command()
    @commands.guild_only()
    async def guide(self, ctx):
        try:
            String = "To set up an initial balance or see your current balance use `?balance`\nTo buy units of a stonk, use `?buy X @Y` where X is the amount in credits and Y is the stonk to be bought.\nTo sell units of a stonk, use `?sell X @Y` where X is the amount in units and Y is the stonk to be sold.\nTo see the value of a stonk use `?stonk @Y` where Y is the stonk to be queried."
            await ctx.send(String)
        except Exception as e:
            log_error(e)


    async def on_message(self,message):
        db.insert({'type':'record','user':str(message.author),'guild':str(message.guild),'timestamp':str(message.created_at), 'length':len(message.content)})

def setup(bot):
    bot.add_cog(StonksCog(bot))