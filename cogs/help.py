import discord
from discord.ext import commands

class Help:
    def __init__(self,client):
        self.client = client

    def retrieve_help(self):
        embed=discord.Embed(title=":white_large_square::white_large_square::white_large_square::white_large_square::regional_indicator_h::regional_indicator_e::regional_indicator_l::regional_indicator_p::white_large_square::white_large_square::white_large_square::white_large_square:", description="[**A bot that clones messages from a chosen server into the nexus server. \nWritten in Python.** (Github Repo)](https://github.com/pyHAAA/User-to-Server)", color=self.client.COLOUR)
        
        embed.add_field(name="**NOTE**: only use this bot in a server that you don't care for, it will wipe all existing channels and create new ones during the setup.", value='*Use `>initialize` with a valid config file to setup the bot.*', inline=False)
        embed.add_field(name='\u200b', value=':white_large_square::white_large_square::regional_indicator_c::regional_indicator_o::regional_indicator_m::regional_indicator_m::regional_indicator_a::regional_indicator_n::regional_indicator_d::regional_indicator_s::white_large_square::white_large_square:')
        embed.add_field(name='__Moderation:__', value='`>soft_ban <member>`: the target will be unable to view any channels\n`>soft_unban <member>`: unbans from a soft ban.', inline=False)
        embed.add_field(name='__Configuration:__', value='`>set_username <password> <name>`: changes the username of the userclient.\n`>info`: displays some useful information.\n`>set_server (id <serverid>)`: sets the server_id without editing the config file.\n`>example_config`: a text config file.\n`>set_config`: use this command with an attached config file.\n`>get_config`: returns the current config file.\n`>reload_config`: reloads the config file (use `>initialize` after a serverid change.)', inline=False)
        embed.add_field(name='__Setup:__', value='`>initialize`: a combination of `>restart` and `>init_channels`.\n`>restart`: wipes all channels from a server, and recreates the control-panel.\n`>init_channels`: creates the respective channels.', inline=False)
        embed.add_field(name='__Colour:__', value='`>colour`: displays the RGB values of the current embed colour.\n`>set_colour <r> <g> <b>`: sets the colour of embeds.', inline=False)
        embed.add_field(name='__Utilities:__', value='`>pause`: pauses monitoring messages - use `>resume` to resume.\n`>resume`: resumes monitoring messages - use `>pause` to pause.\n`>role <role>`: gives you the specified role. (cApS sensitive!)\n`>remove_role <role>`: removes the specified role. (cApS sensitive!)\n`>show_history <limit=50>`: shows the last <limit> messages, locks the channel.')
        embed.add_field(name='__Help:__', value='`>help`: help message.\n`>dm_help`: DMs you the help message.', inline=False)

        return embed

    @commands.command()
    async def dm_help(self,ctx):
        embed=discord.Embed(title="Help message sent.", description="Check your DMs. :e_mail:", color=self.client.COLOUR)
        await ctx.send(embed=embed)

        await ctx.author.send(embed=self.retrieve_help())

    @commands.command()
    async def help(self,ctx):
        await ctx.send(embed=self.retrieve_help())

def setup(client):
    client.add_cog(Help(client))