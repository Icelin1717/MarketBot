import discord
from discord import app_commands
from discord.ext import commands, tasks
import json
from datetime import datetime
import os

with open(file='./config.json', mode='r', encoding='UTF-8') as jfile:
    config = json.load(jfile)

class WebhookEvent(commands.Cog):
    
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        self.webhook_event = {}

        # If 'webhook_event.json' doesn't exist, create it.
        if not os.path.isfile('webhook_event.json'):
            with open(file='webhook_event.json', mode='w+', encoding='UTF-8') as jfile:
                json.dump(self.webhook_event, jfile)
        # Load 'webhook_event.json'
        else:
            with open(file='webhook_event.json', mode='r', encoding='UTF-8') as jfile:
                self.webhook_event = json.load(jfile)                

    # save webhook event to 'webhook_event.json'
    # TODO: switch the webhook event to external DB
    def save_event(self):
        with open(file='webhook_event.json', mode='w', encoding='UTF-8') as jfile:
            json.dump(self.webhook_event, jfile)

    # TODO: switch the webhook event to external DB
    def read_event(self):
        with open(file='webhook_event.json', mode='r', encoding='UTF-8') as jfile:
            self.webhook_event = json.load(jfile)


    """
    ! special methods
    These methods will be automatically called on some specific event.
    cog_load is called when this Cog class is loaded.
    cog_unload is called when it is unloaded.
    """
    def cog_load(self):
        print('Extension "WebhookEvent" has been loaded')
    def cog_unload(self):
        print('Extension "WebhookEvent" has been unloaded')


    # list all existing webhook events
    @app_commands.command(name="list_webhook_event", description="list all existing webhook events")
    @commands.is_owner()
    async def list_webhook_event(self, interaction: discord.Interaction):
        self.read_event()
        message = "```\n"

        guild = self.bot.get_guild(self.config["guildId"])
        for event_name, role_id in self.webhook_event.items():
            role = discord.utils.get(guild.roles, id=role_id)
            if role:
                message += event_name + ": " + role.name + "\n"
            else:
                message += event_name + ": " + str(role_id) + "(找不到此ID的身分組)\n"

        message += "```"
        await interaction.response.send_message(message)
        

    # add a new webhook event
    @app_commands.command(name="add_webhook_event", description="add a new webhook event")
    @app_commands.describe(event_name="The name to trigger event", role="The role to give when a user trigger this event")
    @commands.is_owner()
    async def add_webhook_event(self, interaction: discord.Interaction, event_name: str, role: discord.Role):
        if event_name in self.webhook_event:
            await interaction.response.send_message("失敗。這個事件名稱已被使用過了")
            return
        
        self.webhook_event[event_name] = role.id
        await interaction.response.send_message(f"已新增事件{event_name}，欲新增的身分組：{role.name}")
        self.save_event()


    # remove a webhook event
    @app_commands.command(name="remove_webhook_event", description="remove a webhook event")
    @app_commands.describe(event_name="The name to trigger event")
    @commands.is_owner()
    async def remove_webhook_event(self, interaction: discord.Interaction, event_name: str):
        if event_name not in self.webhook_event:
            await interaction.response.send_message("失敗。這個事件名稱不存在")
            return
        
        del self.webhook_event[event_name]
        await interaction.response.send_message(f"已移除事件{event_name}")
        self.save_event()


    # listen for messages from webhook with a prifix 'Webhook Event'
    @commands.Cog.listener()
    async def on_message(self, msg):
        self.read_event()
        if (msg.webhook_id is not None) and (msg.content.startswith("Webhook Event")):  # if the message is sent by WebhookEvent
            try:
                index = msg.content.split("\n")
                event_name = index[1]
                username = index[2].split("#")
                guild = self.bot.get_guild(self.config["guildId"])
                user = discord.utils.get(guild.members, name=username[0], discriminator=username[1])
                
                if event_name in self.webhook_event:
                    role_id = self.webhook_event[event_name]
                    role = discord.utils.get(guild.roles, id=role_id)
                    await user.add_roles(role)
                    print(f"{user.name} trigger webhook event '{event_name}'")
                    await msg.reply(f"成功添加身分組 '{role.name}'")
                else:
                    await msg.reply("無法識別事件名稱")
            except Exception as e:
                await msg.reply("訊息格式或內容有誤，無法處理\n錯誤內容:\n" + str(e))


async def setup(bot):
    global config
    await bot.add_cog(WebhookEvent(bot, config))