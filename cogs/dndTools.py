import discord
from discord.ext import commands



class DnDCog:
    """ControlCogCog"""

    def __init__(self, bot):
        self.bot = bot

    @client.command(name='bank',
                    pass_context=True,
                    description="Handles the balance of a characters money limited by user ID. Searchable by naming the character.",
                    brief="Handles the balance of a characters money",
                    aliases=['Bank'])
    async def bank(context,*character,**action):
        try:
            with open('bank.csv') as csvfile:
                reader = csv.DictReader(csvfile)
                flag=0
                for row in reader:
                    if row['Character'].find(''.join(character).title())!=-1 and str(context.message.author)==row['Id'] :
                        flag=1
                        await client.say(row['Character'] + ' has: ' + row['Platinum']+' Platinum, '+ row['Gold']+' Gold, '+ row['Silver']+' Silver, and '+ row['Copper']+' Copper')
                if (flag==0):
                    await client.say('Character: "'+''.join(character)+'" not found under your user: '+ str(context.message.author))
        except:
            await client.say("You dun :truck:'d up")

    global rolls
    rolls=[]

    @client.command(name='roll',
                    description="Records rolls on d20s, record rolls with 'add' and plot rolls with 'plot'. Rolls can be cleared with 'clear' or printed with 'list'.",
                    brief="Records rolls on d20s",
                    aliases=['Roll'])
    async def roll(command,*roll):
        global rolls
        if command=='add':
            for num in roll[0].split(','):
                if (int(num)<21 and int(num)>0):
                    rolls.append(int(num))  
                else:
                    await client.say('Please add a d20 roll')
            await client.say('Roll(s) added')
        elif command=='plot':
            x=[1,2,3,4,5,6,7,8,9,10,11,12, 13, 14, 15, 16, 17, 18, 19, 20];
            count=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0, 0, 0, 0]

            for i in range(0,len(rolls)):
                for r in range(0,len(x)):
                    if rolls[i]==x[r]:
                        count[r]=count[r]+1

            m=np.mean(rolls)
            n=len(rolls)

            sum=0
            for num in rolls:
                sum=sum+(num-m)**2

            sd=np.sqrt(1/n*sum)

            
            gauss=(sd/0.4)*max(count)*(1/(sd*np.sqrt(2*3.14)))*2.71**(-(1/2)*((np.linspace(0,20,200)-m)/sd)**2)

            plt.bar(x,count)
            plt.plot(np.linspace(0,20,200),gauss,'r')
            plt.xlabel('Rolls')
            plt.ylabel('Count')
            plt.savefig(path+'/rolls.png')
            plt.clf()
            await client.upload(path+"/rolls.png")
        elif command=='clear':
            rolls=[]
            await client.say('cleared')
        elif command=='list':
            await client.say(rolls)
        print(str(command)+' '+str(roll))



def setup(bot):
    bot.add_cog(DnDCog(bot))
