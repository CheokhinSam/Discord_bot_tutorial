import os
import discord
from dotenv import load_dotenv
import json
from discord.ext import commands

class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    # what is ctx, ctx is context
    @commands.command(name="ping")
    async def ping(self, ctx):
        await ctx.send(f'{round(self.bot.latency*1000)}ms')

def setup(bot):
    bot.add_cog(Main(bot))