import discord
import requests
from discord.ext import commands


class SimpleCog:
    """SimpleCog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='repeat', aliases=['copy', 'mimic'])
    async def do_repeat(self, ctx, *, our_input: str):
        await ctx.send(our_input)


    @commands.command(name='add', aliases=['plus'])
    @commands.guild_only()
    async def do_addition(self, ctx, first: int, second: int):
        total = first + second
        await ctx.send('The sum of **'+str(first)+'** and **'+str(second)+'**  is  **'+str(total)+'**')


    @commands.command(name='me')
    @commands.is_owner()
    async def only_me(self, ctx):
        await ctx.send('Hello' +str(ctx.author.mention)+'. This command can only be used by you!!')


    @commands.command(name='embeds')
    @commands.guild_only()
    async def example_embed(self, ctx):
        """A simple command which showcases the use of embeds.

        Have a play around and visit the Visualizer."""

        embed = discord.Embed(title='Example Embed',
                              description='Showcasing the use of Embeds...\nSee the visualizer for more info.',
                              colour=0x98FB98)
        embed.set_author(name='MysterialPy',
                         url='https://gist.github.com/MysterialPy/public',
                         icon_url='http://i.imgur.com/ko5A30P.png')
        embed.set_image(url='https://cdn.discordapp.com/attachments/84319995256905728/252292324967710721/embed.png')

        embed.add_field(name='Embed Visualizer', value='[Click Here!](https://leovoel.github.io/embed-visualizer/)')
        embed.add_field(name='Command Invoker', value=ctx.author.mention)
        embed.set_footer(text='Made in Python with discord.py@rewrite', icon_url='http://i.imgur.com/5BFecvA.png')

        await ctx.send(content='**A simple Embed for discord.py@rewrite in cogs.**', embed=embed)


    @commands.command(name='Convert',
                description="Converts from one currency to another",
                brief="Converts currencies.",
                aliases=['convert','cv'],)
    @commands.guild_only()
    async def convert(self,ctx):
        try:
            base = ctx.message.content.split(' ')[2].upper()
            target = ctx.message.content.split(' ')[3].upper()
            amount = ctx.message.content.split(' ')[1]
            print(str(ctx.message.content.split(' ')))
            url = 'https://v3.exchangerate-api.com/bulk/2cd5b7af7a11620db435eeb2/' + str(base)

            # Making our request
            response = requests.get(url)
            data = response.json()

            # Your JSON object
            await ctx.send(str(   float(amount)*float((data['rates'])[str(target)]) ) + ' '+ str(target))
        except Exception as e:
            logging.ERROR('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e)+'\r\n')
            await ctx.send('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e))
            await ctx.send("is the command in the format `?convert [number] [currency from] [currency to]`? ")

    async def on_member_ban(self, guild, user):
        print(str(user.name)+'-'+str(user.id) +'was banned from '+str(guild.name)+'-'+str(guild.id))


# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case SimpleCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(SimpleCog(bot))
