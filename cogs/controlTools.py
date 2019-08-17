import discord
from discord.ext import commands
import scipy
import numpy
import simpy
import scipy.signal as sig
import matplotlib
import math
from matplotlib import pyplot as plt


class ControlCog:
    """ControlCog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='step',
                    description="Calculates a step response for a transfer function, the parameters of which are separated by commas.\n ?step 1,3 5,6,1",
                    brief="Calculates a step response.",
                    aliases=['Step'],)
    async def step(self,ctx,num: str,den:str):
        try:
            path = '/falconshare/FalconBot'

            num=tuple(map(float,num.split(',')))
            den=tuple(map(float,den.split(',')))

            tf= sig.lti(num,den)
            t, s = sig.step(tf)
            plt.plot(t, s)
            plt.xlabel('Time / s')
            plt.ylabel('Displacement / m')
            plt.savefig(path+'/step.png')
            plt.clf()
            await ctx.send(file=discord.File(path+"/step.png"))
        except Exception as e:
            await ctx.send('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e))
            logging.ERROR('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e)+'\r\n')

    @commands.command(name='IncBlock',
                    description="Basic control problem consisting of a mass on an inclined plane \n A controller may be added as the third argument \n ?InclinedBlock [mass] [slope(degrees)] [controller]",
                    brief="Basic Control Problem",
                    aliases=['InclinedBlock', 'inclinedblock','incblock','Incblock'],)
    async def InclinedBlock(self,ctx,m,slope,controller):
        try:
            path = '/falconshare/FalconBot'

            x_t = 0
            epsilon = 0.001
            n = 1000
            slope = math.radians(int(slope))

            M = float(m)
            Fs = 1
            g = 9.81

            x = [1]
            dx = [0]
            ddx = [(Fs-math.sin(slope)*M*g)/M]
            t = [0]

            t_max = 10
            dt = 0.0001
            for i in range(0,int(t_max/dt)):
                t.append(i*dt) 
                e = x[i]-x_t
                #Fc = -50*e - 10*dx[i]
                Fc = exec( controller in {'__builtins__': {}}, {})

                Fs = -math.copysign(1,dx[i])
                ddx.append((Fc+Fs-math.sin(slope)*M*g)/M)
                dx.append(dx[i]+ddx[i]*dt)
                x.append(x[i]+dx[i]*dt)

                if i>n:
                    if all( abs(item-x_t) < epsilon for item in x[i-n:i] ):
                        Ts = (i-n)*dt
                        break 

            fig = plt.figure(figsize=(10,7))
            plt.subplot(2, 2, 1)
            plt.plot(t, x)
            plt.xlabel('Time (s)')
            plt.ylabel('Position(m)')

            plt.subplot(2, 2, 2)
            plt.plot(t, dx)
            plt.xlabel('Time (s)')
            plt.ylabel('Velocity (m/s)')

            plt.subplot(2, 2, 3)
            plt.plot(t, ddx)
            plt.xlabel('Time (s)')
            plt.ylabel('Acceleration (m/s^2)')

            plt.text(7,1,'Settling Time: ' + str(Ts) +' Seconds')

            #plt.show()
            plt.savefig(path+'/Results.png',dpi=300 )
            plt.clf()
            await ctx.send(file=discord.File(path+"/Results.png"))
        except Exception as e:
            await ctx.send('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e))
            logging.ERROR('**`ERROR:`**'+ str(type(e).__name__) +'-'+ str(e)+'\r\n')

def setup(bot):
    bot.add_cog(ControlCog(bot))
