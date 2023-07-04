import discord
from discord import app_commands
import json
from discord.ext import commands, tasks
import os
import utils

# load config
with open(file='./config.json', mode='r', encoding='UTF-8') as jfile:
    config = json.load(jfile)

intents = discord.Intents.all()
activity = discord.Game(name='斯普拉遁3')
bot = commands.Bot(command_prefix='!', intents=intents, activity=activity)


@bot.event
async def on_ready():
    print('MarketBot is Ready!')

    # load all extensions in ./ext
    for filename in os.listdir('./ext'):
        if filename.endswith('.py'):
            await bot.load_extension(f'ext.{filename[:-3]}')

    # sync application commands
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


# ping command
@bot.tree.command(name="ping", description="Ping the MarketBot")
@app_commands.checks.has_role(config["adminRoleId"])
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message('The bot is working fine!')


# show all loaded extensions
@bot.tree.command(name="show_extensions", description="Show all loaded extensions")
@app_commands.checks.has_role(config["adminRoleId"])
async def show_extensions(interaction: discord.Interaction):
    response = "```\n"
    for ext_name in list(bot.extensions.keys()):
        response += ext_name + "\n"
    response += "```"
    await interaction.response.send_message(response)


# load a cog extension
@bot.tree.command(name="load", description="Load a cog extension")
@app_commands.describe(ext="the extension to load")
@app_commands.checks.has_role(config["adminRoleId"])
async def load(interaction: discord.Interaction, ext: str):
    if(f'{ext}.py' in os.listdir('./ext')):
        try:
            await bot.load_extension(f'ext.{ext}')
            await interaction.response.send_message(f'Extension "{ext}" has been load.')
        except Exception as e:
            await interaction.response.send_message(e)
    else:
        await interaction.response.send_message(f'Failed to load extension "{ext}".')

    # sync application commands
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


# unload a cog extension
@bot.tree.command(name="unload", description="Unload a cog extension")
@app_commands.describe(ext="the extension to unload")
@app_commands.checks.has_role(config["adminRoleId"])
async def unload(interaction: discord.Interaction, ext: str):
    if(f'{ext}.py' in os.listdir('./ext')):
        try:
            await bot.unload_extension(f'ext.{ext}')
            await interaction.response.send_message(f'Extension "{ext}" has been unload.')
        except Exception as e:
            await interaction.response.send_message(e)
    else:
        await interaction.response.send_message(f'Failed to unload extension "{ext}".')

    # sync application commands
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


# reload a cog extension
@bot.tree.command(name="reload", description="Reload a cog extension")
@app_commands.describe(ext="the extension to reload")
@app_commands.checks.has_role(config["adminRoleId"])
async def reload(interaction: discord.Interaction, ext: str):
    if(f'{ext}.py' in os.listdir('./ext')):
        try:
            await bot.reload_extension(f'ext.{ext}')
            await interaction.response.send_message(f'Extension "{ext}" has been reload.')
        except Exception as e:
            await interaction.response.send_message(e)
    else:
        await interaction.response.send_message(f'Failed to reload extension "{ext}".')

    # sync application commands
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


@bot.tree.error
async def error_handler(interaction: discord.Interaction, error):
    print(error)
    if isinstance(error, app_commands.MissingRole):
        await interaction.response.send_message("錯誤：你沒有執行這個指令的權限", ephemeral=True, delete_after=10)
    else:
        await interaction.response.send_message(f"發生了未知的錯誤，請聯繫管理員。\n錯誤訊息:\n{error}", ephemeral=True)


if __name__ == '__main__' :

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
    bot.run(utils.get_bot_token())