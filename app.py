import ollama
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is ready as {bot.user.name}")

@bot.command(name="hello")
async def hello(ctx):
    await ctx.send("Hello, I'm a bot!")

@bot.command(name="ask")
async def ask(ctx, *, message):
    response = ollama.chat(model='qwen2:latest', messages=[
    {
        'role':'system',
        'content':'You are a helpful assistant who provides answers to questions concisely in no more than 5000 words.',
    },
    {
        'role':'user',
        'content':message,
    },
    ])
    await ctx.send(response['message']['content'])

@bot.command(name="summarise")
async def summarise(ctx):
    msgs = [ message.content async for message in ctx.channel.history(limit=10)]
    summarise_prompt = f"""
        Summarise the following messages delimited by 3 backticks:
        ```
        {msgs}
        ```
        """
    response = ollama.chat(model='qwen2:latest', messages=[
        {
            'role':'system',
            'content':'You are a helpful assistant who summarises the provided messages in bullet points concisely in no more than 1000 words.',
        },
        {
            'role':'user',
            'content':summarise_prompt,
        },
    ])
    await ctx.send(response['message']['content'])            

bot.run(os.getenv("DISCORD_TOKEN_KEY"))