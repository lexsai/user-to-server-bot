import sys
import traceback
import asyncio
import os
import re
import io
from pathlib import Path

import discord
from discord.ext import commands
import json

if __name__ == '__main__': 

    extensions = ['cogs.initialization.setup',
                  'cogs.initialization.config',
                  'cogs.utilities.colour',
                  'cogs.utilities.moderation',
                  'cogs.utilities.play_pause',
                  'cogs.utilities.roles',
                  'cogs.control',
                  'cogs.help']

    bot_client = commands.Bot(command_prefix = '>')
    
    try: 
        with open(str(Path('config.json')), 'r') as config_file: 
            bot_client.CONFIG = json.load(config_file)

    except JSONDecodeError:
        print('INVALID CONFIG FILE')    
        sys.exit()  

    bot_client.user_client = commands.Bot(command_prefix = bot_client.CONFIG['user_token'])

    bot_client.MONITOR = True  


    bot_client.remove_command('help')
    bot_client.user_client.remove_command('help')

    try:
        with open(str(Path('data/colour.json')), 'r') as colour_file:
            colour = json.load(colour_file)

            if colour['r'] > 255:
                colour['r'] = 255
            if colour['g'] > 255:
                colour['g'] = 255
            if colour['b'] > 255:
                colour['b'] = 255

            if colour['r'] < 0:
                colour['r'] = 0
            if colour['g'] < 0:
                colour['g'] = 0
            if colour['b'] < 0:
                colour['b'] = 0
            
            bot_client.COLOUR = discord.Colour.from_rgb(colour['r'], colour['g'], colour['b'])
    except JSONDecodeError:
        print('INVALID COLOUR FILE')    
        sys.exit()  

    print('---')
    for extension in extensions:
        try:
            bot_client.load_extension(extension)
            print(f'"{extension}" loaded for bot client. ({extensions.index(extension)+1}/{len(extensions)})')
        except:
            print(f'Failed to load extension {extension} for bot client.')
            traceback.print_exc()

    print('---')

async def string_clean_content(ctx,input_string):
    """

    uses a custom regex to match all types of mentions, while capturing the id.
    the id is then replaced with a mention to the corresponding role in the nexus server, or just plaintext name.
    """

    for mentionid in [int(match) for match in re.findall(r'<(?:@|@!|@&|#)(\d{16,21})>',input_string)]:
        role = ctx.guild.get_role(mentionid)
        member = ctx.guild.get_member(mentionid)
        channel = ctx.guild.get_channel(mentionid)

        try:
            input_string = input_string.replace(role.mention, discord.utils.get(bot_client.nexus_guild.roles, name=role.name).mention)
        except AttributeError:
            try:
                input_string = input_string.replace(str(member.id), member.name)
            except AttributeError:
                input_string = input_string.replace(channel.mention, discord.utils.get(bot_client.nexus_guild.channels, name=channel.name).mention)

        return input_string

async def message_parser(message,corresponding_channel):
    ctx = await bot_client.user_client.get_context(message)
        
    for member in message.mentions:
        message.content = message.content.replace(str(member.id), member.name)

    for role in message.role_mentions:
        message.content = message.content.replace(role.mention, discord.utils.get(bot_client.nexus_guild.roles, name=role.name).mention)

    for channel in message.channel_mentions:
        message.content = message.content.replace(channel.mention, discord.utils.get(bot_client.nexus_guild.channels, name=channel.name).mention)

    try:
        embed = message.embeds[0]

        if embed.title:
            embed.title = await string_clean_content(ctx,embed.title)

        if embed.description:
            embed.description = await string_clean_content(ctx,embed.description)

        for field in embed.fields:
            field.name = await string_clean_content(ctx,field.name)
            field.value = await string_clean_content(ctx,field.value)

        await corresponding_channel.send(message.content, embed=embed)

    except IndexError:
        try:
            await corresponding_channel.send(message.content)
        except:
            traceback.print_exc()

    for attachment in message.attachments:
        file_like = io.BytesIO()
        await attachment.save(file_like)
        try:
            await corresponding_channel.send(file=discord.File(file_like, filename=attachment.filename))
        except:
            traceback.print_exc()

    await bot_client.process_commands(message)

@bot_client.event
async def on_ready():
    print('Bot client logged in as:')
    print(f'"{bot_client.user.name}" (userID is "{bot_client.user.id}")')
    print('---')
    print(f'Connected servers [{len(bot_client.guilds)}]:')
    for server in bot_client.guilds:
        await server.me.edit(nick='The Cloner.')
        print(server)   
    print('---')
    await bot_client.user.edit(username='The Cloner.')

    await bot_client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=bot_client.user_client.get_guild(bot_client.CONFIG['server_id']).name))

@bot_client.user_client.event
async def on_ready():
    await bot_client.wait_until_ready()

    bot_client.nexus_guild = bot_client.get_guild(bot_client.CONFIG['nexus_id'])
    bot_client.user_client.chosen_guild = bot_client.user_client.get_guild(bot_client.CONFIG['server_id'])
    
    print('User client logged in as:')
    print(f'"{bot_client.user_client.user.name}" (userID is "{bot_client.user_client.user.id}")')
    print('---')
    if bot_client.user_client.get_guild(bot_client.CONFIG['server_id']) in bot_client.user_client.guilds:
        print('Chosen server is viewable.')
    else:
        print('Chosen server is unable to be viewed.')
        sys.exit()
    print('---')


@bot_client.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.errors.CheckFailure):
        embed = discord.Embed(title="Error. :thumbsdown:", colour=bot_client.COLOUR, description='You need the `Cleared` role to use commands.')
        await ctx.send(embed=embed)

    else:
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

@bot_client.check
async def allow_cleared_role(ctx):
    allowed_commands = ['help',
                        'dm_help',
                        'info',
                        'example_config',
                        'colour',
                        'show_history']


    special_role = discord.utils.get(bot_client.nexus_guild.roles, name="Cleared")
    member_nexus = discord.utils.get(bot_client.nexus_guild.members, id=ctx.author.id)

    return special_role in member_nexus.roles or ctx.command.name in allowed_commands

@bot_client.command()
async def show_history(ctx,limit:int):
    if limit > 50:
        limit = 50

    corresponding_channel = discord.utils.get(bot_client.user_client.chosen_guild.channels, name=ctx.message.channel.name)
    
    await ctx.message.channel.set_permissions(bot_client.nexus_guild.default_role, send_messages=False)
    
    embed = discord.Embed(title="Recounting messages.", colour=bot_client.COLOUR, description=f'*The channel will be locked meanwhile.*')
    await ctx.message.channel.send(embed=embed)

    messages = 0

    bot_member = bot_client.nexus_guild.me    

    try:
        async for message in corresponding_channel.history(limit=limit, reverse=True):
            if not bot_client.nexus_guild.get_member(bot_client.user.id).display_name == f'{message.author.display_name} (recounting)':
                try:
                    await bot_member.edit(nick=f'{message.author.display_name} (recounting)')
                except discord.errors.HTTPException:
                    message.content += ' *(Recounting)*'

            await message_parser(message, ctx.message.channel)
            messages += 1

        await ctx.message.channel.set_permissions(bot_client.nexus_guild.default_role, send_messages=True)

    except:
        traceback.print_exc()
    
    embed = discord.Embed(title=f"Finished recounting - {messages} messages.", colour=bot_client.COLOUR, description=f'*The channel will be unlocked.*')
    await ctx.send(embed=embed)

@bot_client.user_client.event
async def on_message(message):
    ctx = await bot_client.get_context(message)

    if message.author == bot_client.user_client.user:
        return

    if bot_client.MONITOR and not ctx.valid and bot_client.is_ready() and bot_client.user_client.is_ready():
        bot_member = bot_client.nexus_guild.me
        
        if not message.guild: #if DMChannel
            if not discord.utils.get(bot_client.nexus_guild.channels, name=str(message.author.id)):
                dm_channel = await bot_client.nexus_guild.create_text_channel(str(message.author.id), topic=f'Check the pinned message for information.', category=discord.utils.get(bot_client.nexus_guild.categories,name='DMs.',position=1))

                author_profile = await bot_client.user_client.get_user_profile(message.author.id)

                mutual_guilds = author_profile.mutual_guilds
                mutual_guild_names = [guild.name for guild in mutual_guilds]

                embed = discord.Embed(title=f"__DM Channel Initialized.__ :thumbsup:", colour=bot_client.COLOUR, description=f'**__User ID__**: {message.author.id}\n**__Name__**: "{message.author.name}"')
                
                embed.add_field(name="__Mutual Guilds:__", value='\n'.join(mutual_guild_names), inline=False)
                
                avatar = message.author.avatar_url
                embed.set_thumbnail(url = avatar)
                
                dm_info = await dm_channel.send(embed=embed)
                await dm_info.pin()

            corresponding_channel = discord.utils.get(bot_client.nexus_guild.channels,name=str(message.author.id),category=discord.utils.get(bot_client.nexus_guild.categories,name='DMs.',position=1))

            if not bot_member.display_name == message.author.name:
                await bot_member.edit(nick=message.author.name)

            await message_parser(message,corresponding_channel)

        elif message.guild == bot_client.user_client.chosen_guild and not message.author.id == bot_client.user_client.user.id:
            corresponding_channel = discord.utils.get(bot_client.nexus_guild.channels,name=message.channel.name)

            if not bot_member.display_name == message.author.display_name:            
                await bot_member.edit(nick=message.author.display_name)
    
            await message_parser(message,corresponding_channel)

@bot_client.event
async def on_message(message):
    ctx = await bot_client.get_context(message)

    if bot_client.MONITOR and not ctx.valid and bot_client.is_ready() and bot_client.user_client.is_ready():
        if message.guild == bot_client.nexus_guild and message.author.id != bot_client.user.id and not message.channel.name == 'control-panel':
            if message.channel.category == discord.utils.get(bot_client.nexus_guild.categories,name='DMs.',position=1):
                corresponding_channel = bot_client.user_client.get_user(int(message.channel.name))

                await message_parser(message,corresponding_channel)
            else:
                corresponding_channel = discord.utils.get(bot_client.user_client.chosen_guild.channels,name=message.channel.name)
                
                bot_member = bot_client.user_client.chosen_guild.me
                try:
                    await bot_member.edit(nick=message.author.display_name) 
                except discord.errors.Forbidden:
                    pass

                await message_parser(message,corresponding_channel)

    await bot_client.process_commands(message)

@bot_client.user_client.event
async def on_typing(channel,user,when):
    if bot_client.MONITOR:
        bot_member = bot_client.nexus_guild.me

        if isinstance(channel,discord.DMChannel):
            if not bot_member.display_name == user.name:
                await bot_member.edit(nick=user.name)

            corresponding_channel = discord.utils.get(bot_client.nexus_guild.channels, name=str(user.id), category=discord.utils.get(bot_client.nexus_guild.categories,name='DMs.',position=1))
            await corresponding_channel.trigger_typing()

        elif not isinstance(channel,discord.DMChannel) and channel.guild == bot_client.user_client.chosen_guild and not channel.id == bot_client.user_client.user.id:
            if not bot_member.display_name == user.display_name:
                await bot_member.edit(nick=user.display_name)

            corresponding_channel = discord.utils.get(bot_client.nexus_guild.channels,name=channel.name)
            await corresponding_channel.trigger_typing()

loop = asyncio.get_event_loop()

loop.create_task(bot_client.user_client.start(bot_client.CONFIG['user_token'],bot=False))
loop.create_task(bot_client.start(os.environ['BOT_TOKEN'],bot=True,reconnect=True))

loop.run_forever()