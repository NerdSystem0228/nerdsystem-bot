from discord import Interaction
from discord.ext import commands
from discord import app_commands
import discord
from discord import Embed
import datetime as dt
class SetAlterFront(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
       
    @commands.command(name="setalterfront")
    async def setalterfront_ctx(self, ctx: commands.Context):
        if not self.bot.whois(ctx.message.author.id):
            await ctx.send(embed=self.create_error_embed("Você não é um membro do NerdSystem"))
            return
        
        first=ctx.message.content.split()[0]
        txt=ctx.message.content.replace(first, "").strip()
        member=None
        if txt.split():
            member=txt.split()[0]
        else:
            member=txt
        memberid=ctx.guild.get_member(int(member.replace("<", "").replace(">", "").replace("@", ""))).id
        member=self.bot.whois(memberid)
        if not member:
            await ctx.send(embed=self.create_error_embed("Este usuário não é um alter do NerdSystem"))
            return
        
        r= await self.bot.APIHttp.set_alter_front(member)
        if isinstance(r, dict):
            await ctx.send(embed=self.create_error_embed(f"{member} já está no front"))
        if r:
            await ctx.send(embed=self.create_message_embed(self.bot.whatcolor(member), member))
        else:
            await ctx.send(embed=self.create_error_embed("Não foi possível se conectar ao Simply Plural API"))
        
    @app_commands.command(
            name = "setalterfront",
            description="Use this command to set to the front")
    async def setalterfront(self, interaction: Interaction, alter: discord.User):
        if not self.bot.whois(interaction.user.id):
            await interaction.response.send_message(embed=self.create_error_embed("Você não é um membro do NerdSystem"), ephemeral=True)
            return 
        
        member=self.bot.whois(alter.id)
        
        if not member:
            await interaction.response.send_message(embed=self.create_error_embed("Este usuário não é um alter do NerdSystem"), ephemeral=True)
            return
        
        r= await self.bot.APIHttp.set_alter_front(member)
        if isinstance(r, dict):
            await interaction.response.send_message(embed=self.create_error_embed(f"{member} já está no front"), ephemeral=True)    
            return
        if r:
            await interaction.response.send_message(embed=self.create_message_embed(self.bot.whatcolor(member), member), ephemeral=True)
        else:
            await interaction.response.send_message(embed=self.create_error_embed("Não foi possível se conectar ao Simply Plural API"), ephemeral=True)
    
    def create_error_embed(self, title):
        embed=Embed(title=title, colour=discord.Colour.red(), timestamp=dt.datetime.now())
        embed.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.avatar.url)
        return embed

    def create_message_embed(self, colour, member):
        embed=Embed(title=f"Você colocou {member} no front!", colour=colour(), timestamp=dt.datetime.now())
        embed.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.avatar.url)
        return embed

async def setup(bot):
    await bot.add_cog(SetAlterFront(bot), guilds=[discord.Object(id=bot.SYSTEM_SERVER)])
