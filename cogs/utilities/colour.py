import discord
from discord.ext import commands
import json
import io
from pathlib import Path

class Colour:
    def __init__(self,client):
        self.client = client

    @commands.command()
    async def set_colour(self,ctx,r:int,g:int,b:int):
        with open(str(Path('data/colour.json')),'r') as colour_file:
            colour = json.load(colour_file)
        
        if r > 255:    
            r = 255
        if g > 255:
            g = 255
        if b > 255:
            b = 255

        if r < 0:
            r = 0
        if g < 0:
            g = 0
        if b < 0:
            b = 0
        
        colour['r'] = r
        colour['g'] = g
        colour['b'] = b

        with open(str(Path('data/colour.json')),'w') as colour_file:
            json.dump(colour,colour_file)
            
        self.client.COLOUR = discord.Colour.from_rgb(colour['r'],colour['g'],colour['b'])
        embed = discord.Embed(title="Colour set. :thumbsup: ", colour=self.client.COLOUR, description=f'<- **R**: {self.client.COLOUR.r}\n<- **G**: {self.client.COLOUR.g}\n<- **B**: {self.client.COLOUR.b}')
        await ctx.send(embed=embed)
    
    @commands.command()
    async def colour(self,ctx):
        embed = discord.Embed(title="Colour. :rainbow:", colour=self.client.COLOUR, description=f'<- **R**: {self.client.COLOUR.r}\n<- **G**: {self.client.COLOUR.g}\n<- **B**: {self.client.COLOUR.b}')
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Colour(client))
    