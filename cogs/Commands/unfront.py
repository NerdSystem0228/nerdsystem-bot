from discord import Interaction
from discord.ext import commands
from discord import app_commands
import discord
from discord import Embed
import datetime as dt
import asyncio
class UnFront(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
       
    @commands.command(name="unfront")
    async def unfront_ctx(self, ctx: commands.Context):
        member=self.bot.whois(ctx.message.author.id)
        if not member:
            await ctx.send(embed=self.create_error_embed("Você não é um alter do NerdSystem"))
            return
        
        r= await self.bot.APIHttp.remove_alter_front(member)  
        if isinstance(r, dict) and r["alreadyonfront"]:
            await ctx.send(embed=self.create_error_embed("Você não está no front"))
            return
        if r:
            await ctx.send(embed=self.create_message_embed(await self.bot.get_member_color(member)))
        else:
            await ctx.send(embed=self.create_error_embed("Não foi possível se conectar ao Simply Plural API"))
        
    async def send_message(self, r, interaction: Interaction, member):
        if isinstance(r, dict) and not r["alreadyonfront"]:
            await interaction.followup.send(embed=self.create_error_embed("Você não está no front"), ephemeral=True)
            return
        if r:
            await interaction.followup.send(embed=self.create_message_embed(await self.bot.get_member_color(member)), ephemeral=True)
        else:
            await interaction.followup.send(embed=self.create_error_embed("Não foi possível se conectar ao Simply Plural API"), ephemeral=True)
                    

    @app_commands.command(
            name = "unfront",
            description="Use this command to enter to the front")
    async def unfront(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True, thinking=True)
        member=self.bot.whois(interaction.user.id)
        if not member:
            await interaction.followup.send(embed=self.create_error_embed("Você não é um alter do NerdSystem"), ephemeral=True)
            return
        
        r=await self.bot.APIHttp.remove_alter_front(member)
        
        await self.send_message(r, interaction, member)

    def create_error_embed(self, title):
        embed=Embed(title=title, color=discord.Color.red(), timestamp=dt.datetime.now())
        embed.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.avatar.url)
        return embed

    def create_message_embed(self, color):
        embed=Embed(title=f"Você saiu do front!", color=color, timestamp=dt.datetime.now())
        embed.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.avatar.url)
        return embed
async def setup(bot):
    await bot.add_cog(UnFront(bot), guilds=[discord.Object(id=bot.SYSTEM_SERVER)])
