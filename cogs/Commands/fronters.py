from discord import Interaction
from discord.ext import commands
from discord import app_commands
import discord
from discord import Embed
import datetime as dt
class Fronters(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
       
    @commands.command(name="fronters")
    async def fronters_ctx(self, ctx: commands.Context):
        await self.bot.APIHttp.get_fronters()
        embeds= self.create_fronters_embeds(self.bot.fronters)
        if embeds:
            await ctx.send(embeds=embeds)
            return
        embed=self.create_error_embed("Ninguém está frontando no momento")
        await ctx.send(embed=embed)
        
    @app_commands.command(
            name = "fronters",
            description="Mostra as alters que estão no front")
    async def fronters(self, interaction: Interaction):
        await self.bot.APIHttp.get_fronters()
        embeds= self.create_fronters_embeds(self.bot.fronters)
        if embeds:
            await interaction.response.send_message(embeds=embeds)
            return
        embed=self.create_error_embed("Ninguém está frontando no momento")
        await interaction.response.send_message(embed=embed)
     
    def create_error_embed(self, title):
        embed=Embed(title=title, color=discord.Color.red())
        embed.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.avatar.url)
        return embed    
    def create_fronters_embeds(self, fronters):
        embedList=[]
        print(fronters)
        for i in fronters:
            print(i)
            embed=Embed(title=i, color=self.bot.whatcolor(i)(), timestamp=dt.datetime.fromtimestamp(fronters[i]["front"]["startTime"]/1000.0))
            embed.set_footer(text="Está frontando desde", icon_url= self.bot.get_guild(self.bot.SYSTEM_SERVER).get_member(self.bot.members[i]["dcid"]).avatar.url)
            embedList.append(embed)
        return embedList

async def setup(bot):
    await bot.add_cog(Fronters(bot), guilds=[discord.Object(bot.SYSTEM_SERVER)])
