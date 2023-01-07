import discord
import json
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv

# load .env if exist & load enviroment variables
load_dotenv()
env_var = os.environ

# load config
with open(file='./config.json', mode='r', encoding='UTF-8') as jfile:
    config = json.load(jfile)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print('MarketBot is Ready!')

    # load all extensions in ./ext
    for filename in os.listdir('./ext'):
        if filename.endswith('.py'):
            await bot.load_extension(f'ext.{filename[:-3]}')

@bot.command()
@commands.is_owner()
async def ping(ctx):
    await ctx.send('The bot is working fine!')

# load a cog extension
@bot.command()
@commands.is_owner()
async def load(ctx, *args):
    for ext in args:
        if(f'{ext}.py' in os.listdir('./ext')):
            await bot.load_extension(f'ext.{ext}')
            await ctx.send(f'Extension "{ext}" has been load.')
        else:
            await ctx.send(f'Failed to load extension "{ext}".')

# unload a cog extension
@bot.command()
@commands.is_owner()
async def unload(ctx, *args):
    for ext in args:
        if(f'{ext}.py' in os.listdir('./ext')):
            await bot.unload_extension(f'ext.{ext}')
            await ctx.send(f'Extension "{ext}" has been unload.')
        else:
            await ctx.send(f'Failed to unload extension "{ext}".')

# reload a cog extension
@bot.command()
@commands.is_owner()
async def reload(ctx, *args):
    for ext in args:
        if(f'{ext}.py' in os.listdir('./ext')):
            await bot.reload_extension(f'ext.{ext}')
            await ctx.send(f'Extension "{ext}" has been reload.')
        else:
            await ctx.send(f'Failed to reload extension "{ext}".')

if __name__ == '__main__' :

    # check if TOKEN env_var exist
    if 'TOKEN' not in env_var:
        print(f"Error: enviroment variable TOKEN is missing")
        quit()

    # check config params
    with open(file='./config_requirements.json', mode='r', encoding='UTF-8') as jfile:
        configRequirement = json.load(jfile)
    for param in configRequirement["requirements"]:
        try:
            check = config[param]
        except KeyError as e:
            print(f"Error: missing config parameter: {param}")
            quit()
    
    # start the bot
    bot.run(env_var['TOKEN'])