import discord
from discord.ext import commands
import pandas as pd
import os
import requests
import datetime
import logging
import traceback
import matplotlib
from matplotlib import pyplot as plt

class DataCog:
	"""ControlCogCog"""

	def __init__(self, bot):
		self.bot = bot

	global debuglv
	debuglv = 0

	global data
	global datapath
	global imagepath

	datapath = '/falconshare/FalconBot/data/'
	imagepath = '/falconshare/FalconBot/images/'

	@commands.command(name='loaddata',
	                description="Loads data from a .csv file and stores it in local memory",
	                brief="Load attached .csv into bot.",
	                aliases=['ld','Ld','Load'])
	async def load_data(self,ctx,*name):
		try:
			await ctx.send('Attempting to Load data')
			global data
			global datapath
			name = str(name[0])

			if not os.path.isfile(datapath+name+'.csv'):
				url=ctx.message.attachments[0].url
				if url.endswith('.csv'):
					r = requests.get(url, allow_redirects=True)
					open(datapath+name +'.csv', 'wb').write(r.content)
					data = pd.read_csv(datapath+name+'.csv')
					summary = "`"+url+"` saved to: "+name+'.csv as:\n```'+str(data[0:5])+'\n...\n...\n'+str(data[len(data)-5:len(data)])+'```'
					if len(summary)>2000:
						await ctx.send('Dataset is too large to print a summary')
					else:
						await ctx.send(summary)
				else:
					await ctx.send('File is not a .csv')
			else:
				await ctx.send(name+'.csv already exists')
				data = pd.read_csv(datapath+name+'.csv')
				summary = name+'.csv loaded as:\n```'+str(data[0:5])+'\n...\n...\n'+str(data[len(data)-5:len(data)])+'```'
				if len(summary)>2000:
					await ctx.send('Dataset is too large to print a summary')
				else:
					await ctx.send(summary)	
		except Exception as e:
			await self.log_error(ctx,e)
            

	@commands.command(name='lineplot',
	                description="",
	                brief="Plots sequential data loaded into the bot",
	                aliases=['lplt', 'plot'])
	async def lineplot(self,ctx,y,*x):
		
		try: 
			global data
			if x:
				plt.plot(data[x[0]],data[y],linewidth=1)
				plt.xlabel(str(x[0]))
				plt.ylabel(str(y))
			else:
				plt.plot(data[y],linewidth=1)
				plt.xlabel('Sample')
				plt.ylabel(str(y))
			plt.savefig(imagepath+'/data.png',dpi=600)
			plt.clf()
			await ctx.send(file=discord.File(imagepath+"data.png"))
		except Exception as e:
			await self.log_error(ctx,e)
            
	@commands.command(name='scatterplot',
	                description="",
	                brief="Plots data loaded into the bot",
	                aliases=['splt'])
	async def scatterplot(self,ctx,y,*x):
		
		try: 
			global data
			if x:
				plt.scatter(data[x[0]],data[y])
				plt.xlabel(str(x[0]))
				plt.ylabel(str(y))
			else:
				plt.scatter(data[y])
				plt.xlabel('Sample')
				plt.ylabel(str(y))
			plt.savefig(imagepath+'/data.png',dpi=600)
			plt.clf()
			await ctx.send(file=discord.File(imagepath+"data.png"))
		except Exception as e:
			await self.log_error(ctx,e)


	@commands.command(name='datasets',
	                description="",
	                brief="Returns all available datasets",
	                aliases=['data', 'Data'])
	async def datasets(self,ctx):
		try: 
			global data
			datalist = "```\r\n"
			filenames = os.listdir(datapath)
			for item in filenames:
				datalist = datalist+str(item)+"\r\n"
			datalist = datalist+"```"
			await ctx.send(datalist)
		except Exception as e:
			await self.log_error(ctx,e)
            
	@commands.command(name='labels',
	                description="",
	                brief="Returns labels from the selected dataset",
	                aliases=['lab'])
	async def labels(self,ctx):
		headings = ''
		for heading in list(data):
			headings = headings+heading+'\r\n'
		await ctx.send(headings)		


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
	bot.add_cog(DataCog(bot))


