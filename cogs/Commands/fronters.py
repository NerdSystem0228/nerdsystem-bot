from discord import Interaction
from discord.ext import commands
from bot import bot
from discord import app_commands
from utils.sp_apihttp import get_fronters, get_member_color
import discord
from discord import Embed
import datetime as dt
class Fronters(commands.Cog):
    def __init__(self):
        pass
       
    @commands.command(name="fronters")
    async def fronters_ctx(self, ctx: commands.Context):
        await get_fronters()
        embeds=await self.create_fronters_embeds(bot.fronters)
        if embeds:
            await ctx.send(embeds=embeds)
            return
        embed= self.create_error_embed("Ninguém está frontando no momento")
        await ctx.send(embed=embed)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.command(name="fronters", description="Mostra as alters que estão no front")
    async def fronters(self, interaction: Interaction):
        await interaction.response.defer(thinking=True)
        await get_fronters()
        embeds=await self.create_fronters_embeds(bot.fronters)
        if embeds:
            await interaction.followup.send(embeds=embeds)
            return
        embed=self.create_error_embed("Ninguém está frontando no momento")
        await interaction.followup.send(embed=embed)
    def create_error_embed(self, title):
        embed=Embed(title=title, color=discord.Color.red())
        embed.set_author(name=bot.user.display_name, icon_url=bot.user.avatar.url)
        return embed
    async def create_fronters_embeds(self, fronters):
        embedList=[]
        for i in fronters:
            embed=Embed(title=i, color=await get_member_color(i), timestamp=dt.datetime.fromtimestamp(fronters[i]["front"]["startTime"]/1000.0))
            embed.set_footer(text="Está frontando desde", icon_url= bot.get_guild(bot.SYSTEM_SERVER).get_member(bot.members[i]["dcid"]).avatar.url)
            embedList.append(embed)
        return embedList

async def setup(bot):
    await bot.add_cog(Fronters())
