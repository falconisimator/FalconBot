import discord
from discord.ext import commands
import pyowm




class WeatherCog:
    """ControlCog"""

    def __init__(self, bot):
        self.bot = bot

    global debuglv
    debuglv = 0
    
    @commands.command()
    @commands.guild_only()
    async def temp(self, ctx, location):
        try:
            api_key = get_file_contents("Keys/OWM.txt")
            owm = pyowm.OWM(api_key)
            observation = owm.weather_at_place(location)
            w = observation.get_weather()
            await ctx.send("Current: " + str(w.get_temperature('celsius')['temp'])+"C\nMax: " + str(w.get_temperature('celsius')['temp_max'])+"C\nMin: " + str(w.get_temperature('celsius')['temp_min'])+"C")
        except Exception as e:
            log_error(e)

    @commands.command()
    @commands.guild_only()
    async def humidity(self, ctx, location):
        try:
            api_key = get_file_contents("Keys/OWM.txt")
            owm = pyowm.OWM(api_key)
            observation = owm.weather_at_place(location)
            w = observation.get_weather()
            await ctx.send("Humidity: "+str(w.get_humidity())+"%" )
        except Exception as e:
            log_error(e)
    

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
    bot.add_cog(WeatherCog(bot))