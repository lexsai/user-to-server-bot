from textwrap import dedent

import discord
from discord.ext import commands

class Control:
    def __init__(self,client):
        self.client = client
     
    @commands.command()
    async def set_username(self,ctx,password,*,choice_name):
        try:
            await self.client.user_client.user.edit(password=password, username=choice_name)
            embed = discord.Embed(title=f"Username set. :thumbsup:", colour=self.client.COLOUR, description=f'New username: "{self.client.user_client.user.name}"')
            await ctx.send(embed=embed)
        except discord.errors.HTTPException:
            embed = discord.Embed(title=f"Error. :thumbsdown:", colour=self.client.COLOUR, description='Incorrect password provided')
            await ctx.send(embed=embed)

    @commands.command()
    async def info(self,ctx):
        server_list = []    
        description_servers = dedent(f"""
                                      **Current target server:** "{self.client.user_client.chosen_guild.name}" (id is {self.client.user_client.chosen_guild.id})
                                      **Current nexus server:** "{self.client.nexus_guild.name}" (id is {self.client.nexus_guild.id})""")

        embed = discord.Embed(title="Server Info: :cloud:", colour=self.client.COLOUR, description=description_servers)
        embed.add_field(name="Account Info: :book:", value=f'**Current user account:** "{self.client.user_client.user.name}" (id is {self.client.user_client.user.id})', inline=False)
        
        for server in self.client.user_client.guilds:
            server_list.append(f'"{server.name}" (id is {server.id})')

        embed.add_field(name="Server list (available to the user account): :white_sun_cloud:", value='\n'.join(server_list), inline=False)
                    
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Control(client))
    
