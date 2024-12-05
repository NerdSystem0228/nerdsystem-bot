from discord import Interaction
from discord.ext import commands
from discord import app_commands
import discord
import os
from dotenv import load_dotenv

load_dotenv()
class Sync(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
       
    @commands.command(name="sync")
    async def status_ctx(self, ctx):
        cmds = await ctx.bot.tree.sync()
        await ctx.send(f"Synced {len(cmds)} commands")

    @app_commands.command(
            name = "sync",
            description="Sync the commands")
    async def sync(self, interaction: Interaction):
        cmds = await self.bot.tree.sync()
        await interaction.response.send_message(f"Synced {len(cmds)} commands")

async def setup(bot):
    await bot.add_cog(Sync(bot), guilds=[discord.Object(id=os.getenv("SYSTEM_SERVER"))])
