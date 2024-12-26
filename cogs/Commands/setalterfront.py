from discord import Interaction
from discord.ext import commands
from bot import bot
from discord import app_commands
from bot import whois
from utils.sp_apihttp import set_alter_front, get_member_color
import discord
from discord import Embed
import datetime as dt
import asyncio
class SetAlterFront(commands.Cog):
    def __init__(self):
        pass
       
    @commands.command(name="setalterfront")
    async def setalterfront_ctx(self, ctx: commands.Context, alter: discord.Member):
        if not whois(ctx.message.author.id):
            await ctx.send(embed=self.create_error_embed("Você não é um membro do NerdSystem"))
            return

        member=whois(alter.id)
        if not member:
            await ctx.send(embed=self.create_error_embed("Este usuário não é um alter do NerdSystem"))
            return
        
        r= await set_alter_front(member)  
        if isinstance(r, dict) and r["alreadyonfront"]:
            await ctx.send(embed=self.create_error_embed(f"{member} já está no front"))
        if r:
            await ctx.send(embed=self.create_message_embed(await get_member_color(member), member))
        else:
            await ctx.send(embed=self.create_error_embed("Não foi possível se conectar ao Simply Plural API"))
        
    async def send_message(self, r, interaction, member):
        if isinstance(r, dict) and r["alreadyonfront"]:
            await interaction.followup.send(embed=self.create_error_embed(f"{member} já está no front"), ephemeral=True)
            return
        if r:
            await interaction.followup.send(embed=self.create_message_embed(await get_member_color(member), member), ephemeral=True)
        else:
            await interaction.followup.send(embed=self.create_error_embed("Não foi possível se conectar ao Simply Plural API"), ephemeral=True)
                
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)    
    @app_commands.command(
            name = "setalterfront",
            description="Use this command to set to the front")
    async def setalterfront(self, interaction: Interaction, alter: discord.User):
        await interaction.response.defer(ephemeral=True, thinking=True)
        if not whois(interaction.user.id):
            await interaction.followup.send(embed=self.create_error_embed("Você não é um membro do NerdSystem"), ephemeral=True)
            return 
        
        member=whois(alter.id)
        
        if not member:
            await interaction.followup.send(embed=self.create_error_embed("Este usuário não é um alter do NerdSystem"), ephemeral=True)
            return
        
        r=await set_alter_front(member)
        
        await self.send_message(r, interaction, member)
        
    def create_error_embed(self, title):
        embed=Embed(title=title, color=discord.Color.red(), timestamp=dt.datetime.now())
        embed.set_author(name=bot.user.display_name, icon_url=bot.user.avatar.url)
        return embed

    def create_message_embed(self, color, member):
        embed=Embed(title=f"Você colocou {member} no front!", color=color, timestamp=dt.datetime.now())
        embed.set_author(name=bot.user.display_name, icon_url=bot.user.avatar.url)
        return embed

async def setup(bot):
    await bot.add_cog(SetAlterFront())
