from discord.ext import commands, tasks
import json
from datetime import datetime

with open(file='./config.json', mode='r', encoding='UTF-8') as jfile:
    config = json.load(jfile)

class ThreadArchiver(commands.Cog):
    
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config


    """
    ! special methods
    These methods will be automatically called on some specific event.
    cog_load is called when this Cog class is loaded.
    cog_unload is called when it is unloaded.
    """
    def cog_load(self):
        print('Extension "ThreadArchiver" has been loaded')
        self.threadArchive.start()
    def cog_unload(self):
        print('Extension "ThreadArchiver" has been unloaded')
        self.threadArchive.stop()


    # Archive unused threads on a regular basis
    @tasks.loop(seconds=config["threadArchiverInterval"])
    async def threadArchive(self):
        print('threadArchiver was called')
        current_time = round(datetime.now().timestamp())

        for channel in [self.bot.get_channel(id) for id in self.config["teamupChannelsId"]]:
            
            if channel == None: continue
            for thread in channel.threads:

                create_time = round(thread.created_at.timestamp())

                if (current_time - create_time) >= self.config['threadTime']:
                    print(f'Locked "{thread.name}" in "{channel.name}"')
                    await thread.edit(archived = True)
            

async def setup(bot):
    global config
    await bot.add_cog(ThreadArchiver(bot, config))