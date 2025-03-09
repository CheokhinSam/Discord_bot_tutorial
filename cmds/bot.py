import ollama
import os
import discord
from dotenv import load_dotenv
import json
from discord.ext import commands

load_dotenv()
CHANNEL_ID = 1340661381199826947

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

# Build a bot
@bot.event
async def on_ready():
    channel = bot.get_channel(CHANNEL_ID)
    print(f"Bot is ready as {bot.user.name}")
    await channel.send(f"Hi, I'm a bot! My name is {bot.user.name}")

# When a member joins the server, send a welcome message (inbox)
@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the MohismLab server, {member.name}!")

# When a member leaves the server, send a leave message (inbox)
@bot.event
async def on_member_remove(member):
    await member.send(f"{member.name} leave!")

# When the bot receives a /hello, it will respond with "Hello, I'm a bot!"
@bot.command(name="hello")
async def hello(ctx):
    await ctx.send("Hello, I'm a bot!")



# send a picture
@bot.command(name="picture")
async def picture(ctx):
    pic = discord.File(os.environ.get("pic"))
    await ctx.send(file=pic)






async def send_long_message(ctx, content):
    if len(content) > 2000:
        for i in range(0, len(content), 2000):
            await ctx.send(content[i:i+2000])
    else:
        await ctx.send(content)

@bot.command(name="ask")
async def ask(ctx, *, message):
    try:
        response = ollama.chat(model='deepseek-r1:1.5b', messages=[
        {'role':'system','content':'You are a helpful assistant who provides answers to questions concisely in no more than 5000 words.',},
        {'role':'user','content':message,},
        ])
        await send_long_message(ctx, response['message']['content'])
    except Exception as e:
        await ctx.send(f"Error happen:{str(e)}")

@bot.command(name="summarise")
async def summarise(ctx):
    try:
        msgs = [ message.content async for message in ctx.channel.history(limit=10)]
        summarise_prompt = f"""
            Summarise the following messages delimited by 3 backticks:
            ```
            {msgs}
            ```
            """
        response = ollama.chat(model='deepseek-r1:1.5b', messages=[
            {'role':'system','content':'You are a helpful assistant who summarises the provided messages in bullet points concisely in no more than 1000 words.',},
            {'role':'user','content':summarise_prompt,},
        ])
        await send_long_message(ctx, response['message']['content'])     
    except Exception as e:
        await ctx.send(f"Error：{str(e)}")


token = os.getenv("DISCORD_TOKEN_KEY")
if not token:
    print("Error：not found DISCORD_TOKEN_KEY")
else:
    bot.run(token)
bot.run(os.getenv("DISCORD_TOKEN_KEY"))