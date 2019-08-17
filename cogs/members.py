import discord
from discord.ext import commands
import time
import praw
import random
import logging
from mcstatus import MinecraftServer

global datapath
datapath = '/falconshare/FalconBot/data/'
global path
path = "/falconshare/FalconBot/"

class MembersCog:
    def __init__(self, bot):
        self.bot = bot

    global debuglv
    debuglv = 0

    @commands.command()
    @commands.guild_only()
    async def joined(self, ctx, *, member: discord.Member):
        """Says when a member joined."""
        await ctx.send(str(member.display_name)+' joined on '+str(member.joined_at))

    @commands.command(name='online')
    async def online(self, context):
        server = MinecraftServer.lookup("ericfalcon.net:25566")
        status = server.status()
        await context.send("'ericfalcon.net:25566' has {0} players and replied in {1} ms".format(status.players.online, status.latency))

    @commands.command(name='github')
    async def github(self, context):
        await context.send("``https://github.com/falconisimator/FalconBot``")
    

    @commands.command(name='coolbot')
    async def cool_bot(self, context):
        """Is the bot cool?"""
        await context.send('This bot is getting cooler! *slowly*...')

    @commands.command(name='instagram',aliases=['insta'])
    async def instagram(self, context):
        """Is the bot cool?"""
        await context.send('https://www.instagram.com/falcon_6280/')


    @commands.command(name='top_role', aliases=['toprole'])
    @commands.guild_only()
    async def show_toprole(self, ctx, *, member: discord.Member=None):
        """Simple command which shows the members Top Role."""

        if member is None:
            member = ctx.author

        await ctx.send('The top role for '+str(member.display_name)+' is '+str(member.top_role.name))
    


    @commands.command(name='perms', aliases=['perms_for', 'permissions'])
    @commands.guild_only()
    async def check_permissions(self, ctx, *, member: discord.Member=None):
        """A simple command which checks a members Guild Permissions.
        If member is not provided, the author will be checked."""

        if not member:
            member = ctx.author

        # Here we check if the value of each permission is True.
        perms = '\n'.join(perm for perm, value in member.guild_permissions if value)

        # And to make it look nice, we wrap it in an Embed.
        embed = discord.Embed(title='Permissions for:', description=ctx.guild.name, colour=member.colour)
        embed.set_author(icon_url=member.avatar_url, name=str(member))

        # \uFEFF is a Zero-Width Space, which basically allows us to have an empty field name.
        embed.add_field(name='\uFEFF', value=perms)

        await ctx.send(content=None, embed=embed)
        # Thanks to Gio for the Command.


    @commands.command(name='ping',
                description="Tests the ping of the bot to the discord servers",
                brief="Tests discord ping.",
                aliases=['pong'])
    @commands.guild_only()
    async def ping(self,ctx):
        try:
            channel = ctx.message.channel
            t1 = time.perf_counter()
            async with ctx.typing():
                t2 = time.perf_counter()
            embed=discord.Embed(title=None, description='Ping: {}'.format(round((t2-t1)*1000)), color=0x2874A6)
            await ctx.send(embed=embed)
        except Exception as e:
            logging.ERROR('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e)+'\r\n')
            await ctx.send('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e))


    @commands.command(name ='morehelp',
                description="Further help",
                brief="Further help and details of the bot")
    @commands.guild_only()
    async def morehelp(self,ctx):
        await ctx.send("http://ericfalcon.net/falconbot-commands/")


    # @client.command(name='decompose',
    #                 description="Prints the properties of the message as seen by the bot.",
    #                 brief="Breaks down a message.",
    #                 aliases=['decomp','Decompose','Decomp'],pass_context=True)
    # async def decompose(context):
    #     properties = {
    #         "context.message.timestamp": context.message.timestamp,
    #         "context.message.content": context.message.content,
    #         "context.message.embeds": context.message.embeds,
    #         "context.message.channel": context.message.channel,
    #         "context.message.server": context.message.server,
    #         "context.message.mentions": context.message.mentions,
    #         "context.message.channel_mentions": context.message.channel_mentions,
    #         "context.message.role_mentions": context.message.role_mentions,
    #         "context.message.id": context.message.id,
    #         "context.message.attachments": context.message.attachments,
    #         "context.message.reactions": context.message.reactions,
    #     }
    #     print(properties);
    #     message = "```"
    #     for k, v in properties.items():
    #         message += k + ": " + str(v) + "\n"

    #     message += "```"
    #     await client.say(message) 

    @commands.command(name='steal',
                    description="Steals an emoji from another server or an image link. Does not work with animated images.",
                    brief="Steals an emoji.",
                    aliases=['Steal'],
                    pass_context=True)
    async def steal(self,ctx, emo, title):
        try:
            emoID=re.findall(r'\d+',emo)[0]
            try:
                url='https://cdn.discordapp.com/emojis/'+emoID
            except:
                await ctx.send("you broke something")
            print(url)
            image=requests.get(url).content
            await ctx.create_custom_emoji(ctx.message.server, name=title, image=image)
            await ctx.send('Emoji stolen :spy:')
        except:
            await ctx.send("You dun :truck:'d up")

    @commands.command(name='kill',
                    description="Makes someone 'ded'",
                    brief="Kills someone.",
                    aliases=['Kill'])
    async def kill(self,ctx):
        try:
            m = ctx.message.mentions[0]
            if(str(m)=='FalconBot#8173'):
                await m.edit(nick = 'FalconBot')
                await ctx.send('No u')
            elif(str(m)!='Falcon#6280'):
                if len(ctx.message.mentions[0].display_name)+4>32:
                    await m.edit(nick = "He's Ded Jim")
                else:
                    await m.edit(nick = 'Ded '+ ctx.message.mentions[0].display_name)
                await ctx.send(ctx.message.mentions[0].mention + 'Killed')
            else:
                await ctx.send('No u')
        except Exception as e:
            await ctx.send('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e))




    @commands.command(name='invite',
                    description="Generates and invite link to the current server",
                    brief="Generates invite.",
                    aliases=['Invite'],)
    async def invite(self,ctx):
        try:
            server = str(ctx.message.guild)
            print(server+' - invite sent')
            if server == 'ControlEngineering':
                link = 'https://discord.gg/PMZ5qRX'
            elif server == 'r/EScapees' or 'Lil Nib Worshippers':
                link = 'https://discord.gg/ZmDWHb2'
            else:
                link = 'Server link not found'+server
            await ctx.send(link)#
        except Exception as e:
            await ctx.send('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e))


    @commands.command(name='eyebleach',
                    description="Posts a cute picture or gif from /r/eyebleach",
                    brief="Generates some eyebleach.",
                    aliases=['brainbleach','Eyebleach'],)
    async def eyebleach(self,ctx):
        try:
            reddit = praw.Reddit(client_id= open(path+"Keys/praw_id.txt", 'r').read().strip(),
                         client_secret=open(path+"Keys/praw_secret.txt", 'r').read().strip(),
                         user_agent="Mysterious")
            memes_submissions = reddit.subreddit('eyebleach').hot()
            post_to_pick = random.randint(1, 100)
            for i in range(0, post_to_pick):
                submission = next(x for x in memes_submissions if not x.stickied)
            await ctx.send(submission.url)
        except Exception as e:
            await ctx.send('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e))

    @commands.command(name='cute',
                    description="Posts a cute picture or gif from various subreddits",
                    brief="Generates some cuteness.",
                    aliases=['Cute','kyoot','kyooot','kyoooot','kyooooot'])
    async def cute(self,ctx):
        try:
            reddit = praw.Reddit(client_id= open(path+"Keys/praw_id.txt", 'r').read().strip(),
                         client_secret=open(path+"Keys/praw_secret.txt", 'r').read().strip(),
                         user_agent="Mysterious")
            subreddits = ['AnimalsBeingJerks',
                            'AnimalTextGifs',
                            'BigCatGifs',
                            'Blep',
                            'CatGifs',
                            'CatPranks',
                            'CatsAreAssholes',
                            'CatLoaf',
                            'CatsAreLiquid',
                            'CatsISUOTTAFTO',
                            'CatsOnGlass',
                            'CatsStandingUp',
                            'CatsWhoYell',
                            'CatsvsTechnology',
                            'CatsWhoSqueak',
                            'CatsWithJobs',
                            'CatTaps',
                            'CurledFeetsies',
                            'HitAnimals',
                            'HoldMyCatnip',
                            'Kittens',
                            'MEOW_IRL',
                            'MicroBork',
                            'MurderMittens',
                            'StartledCats',
                            'StuffOnCats',
                            'ThisIsMyLifeMeow',
                            'TheCatDimension',
                            'TouchThaFishy',
                            'TuckedInKitties',
                            'WhatsWrongWithYourCat']
            subreddit = random.randint(1, 2)
            memes_submissions = reddit.subreddit(subreddits[subreddit]).hot()
            post_to_pick = random.randint(1, 99)
            for i in range(0, post_to_pick):
                submission = next(x for x in memes_submissions if not x.stickied)
            await ctx.send(submission.url)
        except Exception as e:
            await ctx.send('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e))


    @commands.command(name='howdrunkisglass')
    async def howdrunkisglass(self,ctx):
        answers = ['too drunk',
                    'very drunk',
                    'only unable to type',
                    'having a morning soju',
                    "hard to tell, even he doesn't know where he is",
                    "well he's dancing :grimacing:",
                    'Drunk enough to diss xbox',
                    "he's aero, does it make a difference?"]
        await ctx.send(answers[random.randint(1,len(answers))])

    @commands.command(name='howangryispetukka')
    async def howangryispetukka(self,ctx):
        try:
            answers = ['very',
                        'only murderous',
                        'someone is going out a window soon',
                        "There's animals in the building, not just the ones his roomates let in",
                        "only a little, he has his sauna and pictures of tanks <3",
                        'https://www.youtube.com/watch?v=h0ztJzMZbzM ']
            try:
                last
            except NameError:
                last = -1
            number = random.randint(1,len(answers))
            while number == last:
                number = random.randint(1,len(answers))
            last = number
            await ctx.send(answers[number-1])
        except Exception as e:
            await ctx.send('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e))
  

    @commands.command(name = 'notif',aliases=['notifications','notifs'])
    async def notif(self,ctx):
        try:       
            notifications = role = discord.utils.get(ctx.guild.roles, name="notifications")
            await ctx.message.author.add_roles(notifications)
            await ctx.send('Notifications Role Applied')
        except Exception as e:
            await ctx.send('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e)) 

    @commands.command(name = 'helper',aliases=['Helper'])
    async def helper(self,ctx):
        try:       
            Helper = role = discord.utils.get(ctx.guild.roles, name="Helper")
            await ctx.message.author.add_roles(Helper)
            await ctx.send('Helper Role Applied')
        except Exception as e:
            await ctx.send('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e)) 

    @commands.command(name = 'gulag',aliases=['sayhitoknossos','awaywithyou','meditate','noweebshit','reeducateyourself'])
    async def gulag(self,ctx, target, time = 2, unit = 'h'):
        try:       
            timeout = role = discord.utils.get(ctx.guild.roles, name="timeout")
            flag = 0
            for role in ctx.message.author.roles:
                if 'Mod' == role.name:
                    target = ctx.message.mentions[0]
                    flag = 1
                    await target.add_roles(timeout)
                    await ctx.send('Timeout Role Applied')
            if flag == 0:
                await ctx.send('You do not have permission to use this command. This incident will be reported.')
        except Exception as e:
            await ctx.send('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e))         

    @commands.command(name = 'rm_notif')
    async def rm_notif(self,ctx):
        try:       
            notifications = role = discord.utils.get(ctx.guild.roles, name="notifications")
            await ctx.message.author.remove_roles(notifications)
            await ctx.send('Notifications Role Removed')
        except Exception as e:
            await ctx.send('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e))

    @commands.command(name = 'rm_helper')
    async def rm_notif(self,ctx):
        try:       
            Helper = role = discord.utils.get(ctx.guild.roles, name="Helper")
            await ctx.message.author.remove_roles(Helper)
            await ctx.send('Helper Role Removed')
        except Exception as e:
            await ctx.send('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e))

    @commands.command(name = 'gaming')
    async def gaming(self,ctx):
        try:       
            gaming = role = discord.utils.get(ctx.guild.roles, name="Games-n-skribbl")
            await ctx.message.author.add_roles(gaming)
            await ctx.send('Games-n-skribbl Role Applied')
        except Exception as e:
            await ctx.send('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e))        

    @commands.command(name = 'rm_gaming')
    async def rm_gaming(self,ctx):
        try:       
            gaming = role = discord.utils.get(ctx.guild.roles, name="Games-n-skribbl")
            await ctx.message.author.remove_roles(gaming)
            await ctx.send('Games-n-skribbl Role Removed')
        except Exception as e:
            await ctx.send('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e))    

    @commands.command(name = 'color')
    async def color_role(self,ctx,title,color):
        try:
            title = '#'+ title
            roles = ctx.guild.roles
            if not any(role for role in roles if role.name == title):        
                newrole = await ctx.guild.create_role(name = title, color=discord.Color(int(color,0)))
                await ctx.message.author.add_roles(newrole)
                await ctx.send('Role applied as: '+title+' with color'+color)
            else:
                await ctx.send('Role already exists')
        except Exception as e:
            await ctx.send('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e))

    @commands.command(name = 'rm_color',aliases = ['rm'])
    async def removecolor_role(self,ctx,title):
        try:
            title = '#'+ title
            server_roles = ['Approved','D&D','Mod','Deputy','Deputy Deputy']
            for role in ctx.message.author.roles:
                if role.name == title and not role.name in server_roles:
                    await ctx.message.author.remove_roles(role)
                    await role.delete()
                    await ctx.send('Role '+ title +' Removed')
        except Exception as e:
            await ctx.send('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e))

    @commands.command()
    @commands.guild_only()
    async def joke(self, ctx):
        try:
            global datapath
            jokes = open(datapath+"jokes.txt",'r')
            job_titles = [line.decode('utf-8') for line in title_file.readlines()]
            n = len(d)
            jokes.seek(0)
            n = random.randint(1, n)
            await ctx.send(d(n))
            jokes.close()
        except Exception as e:
            logging.ERROR('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e)+'\r\n')
            await ctx.send('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e))


    @commands.command()
    @commands.guild_only()
    async def membercount(self, ctx):
        try:
            Approved = []
            Bots = []
            AFK = []
            for member in ctx.guild.members:
                for role in member.roles: 
                    if role.name == "Approved":
                        Approved.append(member)
                    if role.name == "Emoji Dealers":
                        Bots.append(member)
                    if role.name == "AFK":
                        AFK.append(member)
            AFK = len(AFK)
            Approved = len(Approved)
            Bots = len(Bots)
            await ctx.send(str(Approved-Bots)+" members")
        except Exception as e:
            logging.ERROR('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e)+'\r\n')
            await ctx.send('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e))

    @commands.command()
    @commands.guild_only()
    async def votelims(self, ctx):
        try:
            Approved = []
            Bots = []
            AFK = []
            for member in ctx.guild.members:
                for role in member.roles: 
                    if role.name == "Approved":
                        Approved.append(member)
                    if role.name == "Emoji Dealers":
                        Bots.append(member)
                    if role.name == "AFK":
                        AFK.append(member)
            AFK = len(AFK)
            Approved = len(Approved)
            Bots = len(Bots)
            Members = Approved-Bots-AFK
            await ctx.send(str(int(Members/2+1))+" for Success, "+str(int(Members/4+1)) + " for Fail. \r\n"+str(AFK)+" AFK members excluded.")
        except Exception as e:
            logging.ERROR('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e)+'\r\n')
            await ctx.send('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e))

    # @commands.command(name='afk',
    #                 description="Tests if users have been AFK for more than two weeks",
    #                 brief="AFK tool",
    #                 aliases=['Afk'])
    # async def afk(self,ctx):
    #     try:
    #         author = ctx.message.author.id
    #         members = ctx.guild.members
    #         IDs = []
    #         for member in members:
    #             IDs.append(member.id)
    #         await ctx.send(IDs)
    #         # if(str(author)=='FalconBot#8173'):
    #         #     await m.edit(nick = 'FalconBot')
    #         #     await ctx.send('No u')
    #         # elif(str(m)!='Falcon#6280'):
    #         #     if len(ctx.message.mentions[0].display_name)+4>32:
    #         #         await m.edit(nick = "He's Ded Jim")
    #         #     else:
    #         #         await m.edit(nick = 'Ded '+ ctx.message.mentions[0].display_name)
    #         #     await ctx.send(ctx.message.mentions[0].mention + 'Killed')
    #         # else:
    #         #     await ctx.send('No u')
    #     except Exception as e:
    #         await ctx.send('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e))


    async def on_message(self, message):
        print(str(message.author)+'@'+message.guild.name+' - '+message.channel.name+': '+message.content)
        if message.content.lower().__contains__('hi bot'): # can also use in
            await message.channel.send('Hi '+message.author.display_name)
        # if message.content.lower().__contains__('hi erik'):
        #     await message.channel.send("You meant 'Hi Eric'")
        # if message.content.__contains__('MIT'):
        #     try:
        #         await message.add_reaction(self.bot.get_emoji(520748890182647822))
        #     except Exception as e:
        #         await message.channel.send('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e))      
        if message.content.lower().__contains__('matlab'):
            try:
                await message.add_reaction(self.bot.get_emoji(512699051083431936))
            except Exception as e:
                await message.channel.send('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e))
        if message.content.lower().__contains__('advanced milk'):
            try:
                await message.channel.send('<https://cdn.discordapp.com/attachments/487334904502419488/583643894764535838/video.mov>')
            except Exception as e:
                await message.channel.send('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e))
        if message.content.lower().__contains__('birb'):
            try:
                await message.add_reaction(self.bot.get_emoji(495951725564264458))
            except Exception as e:
                await message.channel.send('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e)) 
        if message.content.lower().__contains__('delta') and message.author.id == 368044646632521729:
            try:
                await message.channel.send('NABLA u pheasant')
            except Exception as e:
                await message.channel.send('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e))
        if message.content.lower().__contains__('nabla') and message.author.id == 300833808410869760:
            try:
                await message.add_reaction(self.bot.get_emoji(545285489461297172))
            except Exception as e:
                await message.channel.send('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e)) 
        if message.content.lower().__contains__('get it girl'):
            try:
                await message.channel.send("https://tenor.com/view/gina-linetti-get-it-girl-gif-9405007")
            except Exception as e:
                await message.channel.send('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e)) 
        if message.content.lower().__contains__('hams') or message.content.lower().__contains__('hamster') or message.content.lower().__contains__('pippi'):
            try:
                await message.add_reaction(self.bot.get_emoji(526847018279370753))
            except Exception as e:
                await message.channel.send('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e))
        if message.content.__contains__("Vote:"):
            try:
                await message.add_reaction(self.bot.get_emoji(547890813741563915))
                await message.add_reaction(self.bot.get_emoji(547890812642525186))
                await message.add_reaction(self.bot.get_emoji(502455948976324618))
            except Exception as e:
                await message.channel.send('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e)) 
        if message.content.lower().__contains__('lil nib'):
            try:
                await message.add_reaction(self.bot.get_emoji(522417825462091786))
            except Exception as e:
                await message.channel.send('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e))

    #async def on_reaction_add(reaction, user)




                

# The setup function below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(MembersCog(bot))

