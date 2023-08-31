import discord
from discord import app_commands, ui
from discord.ext import commands
import json
from datetime import datetime, timedelta, timezone
import utils

with open(file='./config.json', mode='r', encoding='UTF-8') as jfile:
    config = json.load(jfile)

class FeedbackModal(ui.Modal, title='意見回饋'):
    content = ui.TextInput(label="在這邊寫下您的意見", style=discord.TextStyle.paragraph, min_length=3)

    async def on_submit(self, interaction: discord.Interaction):
        stime = datetime.utcnow().replace(tzinfo=timezone.utc)
        time = stime.astimezone(timezone(timedelta(hours=8))).strftime("%Y/%m/%d %H:%M:%S")
        data = [time, interaction.user.name, interaction.user.display_name, self.content.value]
        utils.db_insert("feedback", data)
        await interaction.response.send_message(f'感謝您的回饋！以下是您所提交的內容：```\n{self.content.value}```', ephemeral=True)

class FeedbackView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="開始填寫", style=discord.ButtonStyle.blurple, custom_id="FeedbackView:sendFeedbackModal")
    async def sendFeedbackModal(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_modal(FeedbackModal())



class FeedbackSystem(commands.Cog):
    
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
        self.bot.add_view(FeedbackView())
        print('Extension "FeedbackSystem" has been loaded')
    def cog_unload(self):
        print('Extension "FeedbackSystem" has been unloaded')

    @app_commands.command(name='create_feedback_view', description="產生一個回饋終端")
    @app_commands.checks.has_role(config["adminRoleId"])
    async def create_feedback_view(self, interaction: discord.Interaction):
        await interaction.response.send_message("請點擊下方按鈕以開始填寫回饋", view=FeedbackView())


async def setup(bot):
    global config
    await bot.add_cog(FeedbackSystem(bot, config))