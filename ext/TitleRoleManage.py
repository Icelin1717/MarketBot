import discord
from discord import app_commands
from discord.app_commands import Choice
import json
from discord.ext import commands
import typing
import utils

with open(file='./config.json', mode='r', encoding='UTF-8') as jfile:
    config = json.load(jfile)

class TitleRoleManage(commands.Cog):
    
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        self.guild = self.bot.get_guild(self.config["guildId"])

    """
    ! special methods
    These methods will be automatically called on some specific event.
    cog_load is called when this Cog class is loaded.
    cog_unload is called when it is unloaded.
    """
    def cog_load(self):
        print('Extension "TitleRoleManage" has been loaded')
    def cog_unload(self):
        print('Extension "TitleRoleManage" has been unloaded')


    @app_commands.command(name="new_title", description="新增一種稱號")
    @app_commands.describe(
        name="稱號名稱",
        color="稱號顏色(可輸入色碼#123456或色彩名稱)",
        sort_id="[非必填]稱號排序編號")
    @app_commands.choices(color=[
        Choice(name="X對戰色", value="#0FD496"),
        Choice(name="蠻頹對戰色", value="#FD7400"),
        Choice(name="打工色", value="#F85E3C"),
        Choice(name="打工競賽色", value="#FDD400"),
        Choice(name="light gray", value="#979C9F"),
        Choice(name="magenta", value="#E91E63"),
        Choice(name="red", value="#E74C3C"),
        Choice(name="gold", value="#F1C40F"),
        Choice(name="green", value="#2ECC71"),
        Choice(name="blue", value="#3498DB"),
        Choice(name="dark blue", value="#206694"),
        Choice(name="purple", value="#9B59B6"),
        Choice(name="dark purple", value="#71368A"),
    ])
    @app_commands.checks.has_role(config["adminRoleId"])
    async def new_title(self, interaction: discord.Interaction, name: str, color: Choice[str], sort_id: typing.Optional[int] = 99999999):
        color_obj = discord.Colour.from_str(color.value)
        role = await self.guild.create_role(name=name, colour=color_obj, reason="透過MarketBot指令 'new_title' 建立")
        utils.db_insert("titleRole", [str(sort_id), name, str(role.id)])
        await interaction.response.send_message(f"成功建立稱號 {role.mention}")

    @app_commands.command(name="delete_title", description="刪除一種稱號")
    @app_commands.describe(
        title="欲刪除的稱號"
    )
    @app_commands.checks.has_role(config["adminRoleId"])
    async def delete_title(self, interaction: discord.Interaction, title: discord.Role):
        utils.db_remove("titleRole", "roleId", str(title.id))
        name = title.name
        await title.delete(reason="透過MarketBot指令 'delete_title' 刪除")
        await interaction.response.send_message(f"成功刪除稱號 {name}")
        

async def setup(bot):
    global config
    await bot.add_cog(TitleRoleManage(bot, config))