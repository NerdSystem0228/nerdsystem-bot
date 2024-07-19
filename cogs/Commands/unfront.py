from discord import Interaction
from discord.ext import commands
from discord import app_commands
import discord
from discord import Embed
import datetime as dt
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
        if isinstance(r, dict):
            await ctx.send(embed=self.create_error_embed("Você não está no front"))
            return
        if r:
            await ctx.send(embed=self.create_message_embed(self.bot.whatcolor(member)))
        else:
            await ctx.send(embed=self.create_error_embed("Não foi possível se conectar ao Simply Plural API"))
    

    @app_commands.command(
            name = "unfront",
            description="Use this command to enter to the front")
    async def unfront(self, interaction: Interaction):
        member=self.bot.whois(interaction.user.id)
        if not member:
            await interaction.response.send_message(embed=self.create_error_embed("Você não é um alter do NerdSystem"), ephemeral=True)
            return
        
        r= await self.bot.APIHttp.remove_alter_front(member)
        if isinstance(r, dict):
            await interaction.response.send_message(embed=self.create_error_embed("Você não está no front"), ephemeral=True)
            return
        if r:
            await interaction.response.send_message(embed=self.create_message_embed(self.bot.whatcolor(member)), ephemeral=True)
        else:
            await interaction.response.send_message(embed=self.create_error_embed("Não foi possível se conectar ao Simply Plural API"), ephemeral=True)
    

    def create_error_embed(self, title):
        embed=Embed(title=title, colour=discord.Colour.red(), timestamp=dt.datetime.now())
        embed.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.avatar.url)
        return embed

    def create_message_embed(self, colour):
        embed=Embed(title=f"Você saiu do front!", colour=colour(), timestamp=dt.datetime.now())
        embed.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.avatar.url)
        return embed
async def setup(bot):
    await bot.add_cog(UnFront(bot), guilds=[discord.Object(id=bot.SYSTEM_SERVER)])
