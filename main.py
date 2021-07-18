import discord
import os
import discord.ext
from discord.ext import commands

client = commands.Bot(command_prefix='%', help_command=None)
@client.event
async def on_ready():
  print("bot is ready")

@client.command()
async def hello(ctx):
  await ctx.send('hello')


client.run(os.environ['Token'])
  
