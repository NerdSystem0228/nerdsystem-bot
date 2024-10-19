from discord import Interaction
from discord.ext import commands
from discord import app_commands
import discord
from discord import Embed
import datetime as dt
import asyncio
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
        if isinstance(r, dict) and r["alreadyonfront"]:
            await ctx.send(embed=self.create_error_embed(f"{member} já está no front"))
        if r:
            await ctx.send(embed=self.create_message_embed(await self.bot.get_member_color(member), member))
        else:
            await ctx.send(embed=self.create_error_embed("Não foi possível se conectar ao Simply Plural API"))
        
    async def send_message(self, r, interaction, member):
        if isinstance(r, dict) and r["alreadyonfront"]:
            await interaction.followup.send(embed=self.create_error_embed(f"{member} já está no front"), ephemeral=True)
            return
        if r:
            await interaction.followup.send(embed=self.create_message_embed(await self.bot.get_member_color(member), member), ephemeral=True)
        else:
            await interaction.followup.send(embed=self.create_error_embed("Não foi possível se conectar ao Simply Plural API"), ephemeral=True)
                
    
    @app_commands.command(
            name = "setalterfront",
            description="Use this command to set to the front")
    async def setalterfront(self, interaction: Interaction, alter: discord.User):
        await interaction.response.defer(ephemeral=True, thinking=True)
        if not self.bot.whois(interaction.user.id):
            await interaction.followup.send(embed=self.create_error_embed("Você não é um membro do NerdSystem"), ephemeral=True)
            return 
        
        member=self.bot.whois(alter.id)
        
        if not member:
            await interaction.followup.send(embed=self.create_error_embed("Este usuário não é um alter do NerdSystem"), ephemeral=True)
            return
        
        r=await self.bot.APIHttp.set_alter_front(member)
        
        await self.send_message(r, interaction, member)
        
    def create_error_embed(self, title):
        embed=Embed(title=title, color=discord.Color.red(), timestamp=dt.datetime.now())
        embed.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.avatar.url)
        return embed

    def create_message_embed(self, color, member):
        embed=Embed(title=f"Você colocou {member} no front!", color=color, timestamp=dt.datetime.now())
        embed.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.avatar.url)
        return embed

async def setup(bot):
    await bot.add_cog(SetAlterFront(bot), guilds=[discord.Object(id=bot.SYSTEM_SERVER)])