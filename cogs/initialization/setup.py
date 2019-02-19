import traceback

import discord
from discord.ext import commands

class Setup:
    def __init__(self,client):
        self.client = client

    @commands.command()
    async def init_channels(self,ctx):
        channels_created = 0
        categories_created = 0
        roles_created = 0

        for category in self.client.user_client.chosen_guild.categories:
            if not discord.utils.get(self.client.nexus_guild.categories, name=category.name):
                await self.client.nexus_guild.create_category_channel(category.name)
                categories_created += 1
                for channel in category.channels:
                    if not discord.utils.get(self.client.nexus_guild.channels, name=channel.name):
                        created_category = discord.utils.get(self.client.nexus_guild.categories, name=category.name)
                        await self.client.nexus_guild.create_text_channel(channel.name, category=created_category)
                        channels_created += 1

        for role in self.client.user_client.chosen_guild.roles:
            if not discord.utils.get(self.client.nexus_guild.roles, name=role.name):
                await self.client.nexus_guild.create_role(name=role.name,colour=role.colour)
                roles_created += 1
                
        if not channels_created and not categories_created and not roles_created:
            embed = discord.Embed(title="Already Initialized. :thumbsdown: ", colour=discord.Colour.red(), description=f'Created {channels_created} channels and {categories_created} categories...')
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title="Initialized. :thumbsup: ", colour=self.client.COLOUR, description=f'Created {channels_created} channels, {categories_created} categories and {roles_created} roles.')
            await ctx.send(embed=embed)
    
    @commands.command()
    async def restart(self,ctx):
        channels_deleted = 0
        categories_deleted = 0
        roles_deleted = 0 

        try:    
            for channel in ctx.guild.channels:
                await channel.delete()
                channels_deleted += 1
            
            for category in ctx.guild.categories:
                await category.delete()
                categories_deleted += 1

            for role in ctx.guild.roles:
                if not role.name in ['Cleared','Cloner','@everyone']:
                    await role.delete()
                    roles_deleted += 1

        except:
            traceback.print_exc()

        important_category = await ctx.guild.create_category_channel('All the Servers.')
        control_panel = await ctx.guild.create_text_channel('control-panel',category=important_category)
        help_channel = await ctx.guild.create_text_channel('help',category=important_category)
        
        await ctx.guild.create_category_channel('DMs.')

        await help_channel.set_permissions(ctx.guild.default_role, send_messages=False)
        
        embed = discord.Embed(title="Server Restarted.", colour=self.client.COLOUR, description=f'Deleted {channels_deleted} channels \nDeleted {categories_deleted} categories \nDeleted {roles_deleted} roles.')
        embed.set_thumbnail(url=ctx.guild.icon_url)

        await control_panel.send(embed=embed)

        context_edited = ctx
        context_edited.channel = help_channel

        await context_edited.invoke(self.client.get_command('help'))

    @commands.command()
    async def initialize(self,ctx):
        await ctx.invoke(self.client.get_command('restart'))
        
        context_edited = ctx
        context_edited.channel = discord.utils.get(ctx.guild.channels, name='control-panel')
        
        await context_edited.invoke(self.client.get_command('init_channels'))

def setup(client):
    client.add_cog(Setup(client))
    
