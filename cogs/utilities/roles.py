import discord
from discord.ext import commands

class Roles:
    def __init__(self,client):
        self.client = client
     
    @commands.command()
    async def role(self,ctx,*,role : discord.Role):
        await ctx.author.add_roles(role)

        embed = discord.Embed(title='Role given. :thumbsup:  ', colour=self.client.COLOUR, description=f'Role "**{role.name}**" given.')
        await ctx.send(embed=embed)

    @commands.command()
    async def remove_role(self,ctx,*,role : discord.Role):
        await ctx.author.remove_roles(role)

        embed = discord.Embed(title='Role removed. :thumbsup:  ', colour=self.client.COLOUR, description=f'Role "**{role.name}**" removed.')
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Roles(client))
    
