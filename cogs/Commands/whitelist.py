from discord import Interaction
from discord.ext import commands
from gamercon_async import GameRCON
from discord import Embed
import discord
from bot import data
class Whitelist(commands.Cog):
    def __init__(self):
        pass
    
    @commands.command(name="whitelist")
    async def whitelist_ctx(self, ctx: commands.Context,  name: str):
        client = GameRCON("nerdsystem.me", "25575", data.RCON_PASSWORD, timeout=10)
        async with client as pot_client:
            response = await pot_client.send(f"whitelist add {name}")
            await ctx.send(embed=self.create_whitelist_embed(response))
    async def whitelist(self, interaction: Interaction, name: str):
        await interaction.response.defer(thinking=True)
        
        client = GameRCON("nerdsystem.me", "25575", data.RCON_PASSWORD, timeout=10)
        async with client as pot_client:
            response = await pot_client.send(f"whitelist add {name}")
            await interaction.followup.send(embed=self.create_whitelist_embed(response))
            
    def create_whitelist_embed(self, response):
        if "Player is already whitelisted" in response:
            return Embed(title="Você já foi adicionado ao whitelist do servidor!", color=discord.Color.red().value)
        elif "Added" in response:
            return Embed(title="Você foi adicionado ao whitelist do servidor com sucesso!", color=discord.Color.green().value)
        else:
            return Embed(title="Um problema ocorreu", description="Caso tenha um espaço no nome que colocou, retire e tente novamente", color=discord.Color.red().value)
            
async def setup(bot):
    await bot.add_cog(Whitelist())
