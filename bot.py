import discord
from discord.ext import commands

client = commands.Bot(command_prefix = ".")

@client.event
async def on_ready():
    print('aye aye captain')

@client.command()
async def beep(ctx):
    await ctx.send(f'boop {client.latency * 1000}')


client.run('NzczMzM5MzY0NDQ0MjA5MTc0.X6HyaA.whMtIsCYhj-fYDmCeDpHHKewzBU')

