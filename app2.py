import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

bot = commands.Bot(command_prefix="/")

@bot.event
async def on_ready():
    print(f"Bot is ready as {bot.user.name}")


bot.run(os.getenv("DISCORD_TOKEN_KEY"))