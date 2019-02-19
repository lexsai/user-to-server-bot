from pathlib import Path
import traceback
import io

import discord
from discord.ext import commands
import json

class Config:
    def __init__(self,client):
        self.client = client

    @commands.command()
    async def get_config(self,ctx):
        with open(str(Path('config.json')), 'rb') as config_file:
            embed = discord.Embed(title="Current config file.", colour=self.client.COLOUR, description='Enjoy. :heart:')
            await ctx.send(embed=embed, file=discord.File(config_file))

    @commands.command()
    async def set_config(self,ctx,*,stringchoice = None):
        try:
            file_like = io.BytesIO()
            attachmentObj = ctx.message.attachments[0]
            await attachmentObj.save(file_like)

            try:
                with file_like as ctemp:
                    json.load(ctemp)

                await attachmentObj.save(str(Path('config.json')))
                
                embed = discord.Embed(title="Config file loaded.", colour=self.client.COLOUR, description=':thumbsup:')
                await ctx.send(embed=embed)

            except json.decoder.JSONDecodeError:
                embed = discord.Embed(title="Error. :thumbsdown:", colour=self.client.COLOUR, description='Invalid json file. No changes were made.')
                await ctx.send(embed=embed)

        except:
            traceback.print_exc()
            try:
                configstr_dict = json.loads(stringchoice)

                with open(str(Path('config.json')),'w') as config_file:
                    json.dump(configstr_dict,config_file)
                    embed = discord.Embed(title="Config string loaded.", colour=self.client.COLOUR, description=':thumbsup:')
                    await ctx.send(embed=embed)

            except json.decoder.JSONDecodeError:
                embed = discord.Embed(title="Error. :thumbsdown:", colour=self.client.COLOUR, description='Invalid json. No changes were made.')
                await ctx.send(embed=embed)

    @commands.command()
    async def example_config(self,ctx):
        with open(str(Path('data/config_example.json')),'rb') as config_file:
            embed = discord.Embed(title="Example config file.", colour=self.client.COLOUR, description='*Simply change the values and use `>config` with the attached file.*')
            await ctx.send(embed=embed,file=discord.File(config_file,filename='config_example.json'))

    @commands.command()
    async def reload_config(self,ctx):
        embed = discord.Embed(title="Reloading config file.", colour=self.client.COLOUR, description=':thumbsup:')
        await ctx.send(embed=embed)

        try:
            with open(str(Path('config.json')),'r') as config_file:
                self.client.CONFIG = json.load(config_file)
        
        except json.decoder.JSONDecodeError:
            embed = discord.Embed(title="Error. :thumbsdown:", colour=self.client.COLOUR, description='Invalid json file, input a new config file.')
            await ctx.send(embed=embed)

        self.client.user_client.chosen_guild = self.client.user_client.get_guild(self.client.CONFIG['server_id'])   
        self.client.nexus_guild = self.client.get_guild(self.client.CONFIG['nexus_id'])
        
        if not self.client.user_client.chosen_guild or not self.client.nexus_guild:
            embed = discord.Embed(title="Error. :thumbsdown:", colour=self.client.COLOUR, description='Invalid `nexus_id` or `server_id`, input a new config file.')
            await ctx.send(embed=embed)

        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=self.client.user_client.chosen_guild.name))

    @commands.group(invoke_without_command=True)
    async def set_server(self,ctx):
        server_list = []
        
        for server in self.client.user_client.guilds:
            server_list.append(f'**{self.client.user_client.guilds.index(server)+1})** "{server.name}" (id is {server.id})')

        embed = discord.Embed(title="Choose a number corresponding to the server list.", colour=self.client.COLOUR, description='\n'.join(server_list))
        await ctx.send(embed=embed)

        def check(message):
            return message.content.isdigit() and message.channel == ctx.channel and message.author == ctx.author

        try:
            choice = await self.client.wait_for('message', check=check, timeout=60)
        except asyncio.TimeoutError:
            embed = discord.Embed(title="Error. :thumbsdown:", colour=self.client.COLOUR, description='Timed out, you have to answer in 60 seconds or less!')
            await ctx.send(embed=embed)   
            return

        try:
            guild = self.client.user_client.guilds[int(choice.content) - 1]
        except IndexError:
            embed = discord.Embed(title="Error. :thumbsdown:", colour=self.client.COLOUR, description='Number chosen is out of range. :thinking:')
            await ctx.send(embed=embed)   
            return

        self.client.CONFIG['server_id'] = guild.id
        self.client.user_client.chosen_guild = self.client.user_client.get_guild(self.client.CONFIG['server_id'])   

        with open(str(Path('config.json')),'w') as config_file:
            json.dump(self.client.CONFIG, config_file)

        embed = discord.Embed(title="Server set. :thumbsup:", colour=self.client.COLOUR, description=f'"{self.client.user_client.chosen_guild.name}".')
        await ctx.send(embed=embed)   

        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=self.client.user_client.chosen_guild.name))
        
    @set_server.command(name="id")
    async def _id(self,ctx,server:int):
        self.client.CONFIG['server_id'] = server
        self.client.user_client.chosen_guild = self.client.user_client.get_guild(self.client.CONFIG['server_id'])   

        with open(str(Path('config.json')),'w') as config_file:
            json.dump(self.client.CONFIG,config_file)

        embed = discord.Embed(title="Server set. :thumbsup:", colour=self.client.COLOUR, description=f'**Name of server:** "{self.client.user_client.chosen_guild.name}".')
        await ctx.send(embed=embed)     

        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=self.client.user_client.chosen_guild.name))

def setup(client):
    client.add_cog(Config(client))
    
