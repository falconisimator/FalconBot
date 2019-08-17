import discord
from discord.ext import commands
import asyncio
import time



class PlanningCog:
	"""PlanningCog"""

	def __init__(self, bot):
		self.bot = bot
		self.reminders = fileIO("data/remindme/reminders.json", "load")
		self.units = {"minute" : 60, "hour" : 3600, "day" : 86400, "week": 604800, "month": 2592000}

	async def Background_Counter(bot):
		await bot.wait_until_ready()
		counter = 0
		channel = discord.Object(id='channel_id_here')
		while not client.is_closed:
			counter += 1
			await fitness.send('test')
			await asyncio.sleep(5) # task runs every 60 seconds



	global fitness

	@commands.command(name='set_fitness', hidden=True)
	@commands.is_owner()
	async def Set_Fitness(self, ctx):
		try:
			fitness = ctx.message.channel
			await fitness.send('Fitness set here')
		except Exception as e:
			await ctx.send('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e))
			logging.ERROR('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e)+'\r\n')
			



def setup(bot):
	remind = PlanningCog(bot)
	bot.loop.create_task(PlanningCog.Background_Counter(PlanningCog.bot))
	loop = asyncio.get_event_loop()
	loop.create_task(remind.Background_Counter())
	bot.add_cog(remind)

