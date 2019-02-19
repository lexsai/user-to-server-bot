import discord
from discord.ext import commands

class PausePlay:
    def __init__(self,client):
        self.client = client
        
    @commands.command()
    async def pause(self,ctx):
        self.client.MONITOR = False
        embed = discord.Embed(title='Message cloning paused. :pause_button: ', colour=self.client.COLOUR, description='*Resume with `>resume`*')
        await ctx.send(embed=embed)

    @commands.command()
    async def resume(self,ctx):
        self.client.MONITOR = True
        embed = discord.Embed(title='Message cloning resumed. :play_pause:  ', colour=self.client.COLOUR, description='*Pause with `>pause`*')
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(PausePlay(client))
    
