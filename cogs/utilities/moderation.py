import discord
from discord.ext import commands

class Misc:
    def __init__(self,client):
        self.client = client
        
    @commands.command()
    async def soft_ban(self,ctx,member : discord.Member):
        embed = discord.Embed(title=f'"{member.display_name}" was soft banned. :joy:', colour=self.client.COLOUR, description='*This stops the member from seeing any channels.*')
        await ctx.send(embed=embed)
        for channel in ctx.guild.channels:
            await channel.set_permissions(member, read_messages=False)

    @commands.command()
    async def soft_unban(self,ctx,member : discord.Member):
        embed = discord.Embed(title=f'"{member.display_name}" was unbanned from a soft ban. :joy:', colour=self.client.COLOUR, description='*The member can now see channels again.*')
        await ctx.send(embed=embed)
        for channel in ctx.guild.channels:
            await channel.set_permissions(member, read_messages=True)
    
    @commands.command()
    async def purge(self,ctx,limit : int):
        deleted_messages = await ctx.channel.purge(limit=limit)

        embed = discord.Embed(title="Channel Purged.", colour=self.client.COLOUR, description=f'Delete {len(deleted_messages)} messages.')
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Misc(client))
    
