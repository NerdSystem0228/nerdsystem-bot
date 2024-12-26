from discord.ext import commands
from bot import bot
from discord import Embed
from utils.logger import logger
from bot import bot
import discord
import datetime as dt

class OnMemberJoin(commands.Cog):
    def __init__(self):
        pass
        
    @commands.Cog.listener("on_member_join")
    async def on_member_join(self, member): 
        embed=self.create_welcome_embed(member)
        await bot.get_channel(bot.WELCOME_CHANNEL).send(member.mention, embed=embed)
    
    def create_welcome_embed(self, member):
        embed=Embed(title=f"Bem vindo ao {bot.get_guild(bot.SYSTEM_SERVER).name}!", color=discord.Color.blurple(), timestamp=dt.datetime.now())
        embed.description=f"Espero que goste de sua estadia nesse hospí- quero dizer, lugar com pessoas acolhedoras que tem mente aberta o suficiente para aceitar a existência de uma estrutura neural onde possibilita mais de uma consciência num mesmo cérebro, parabéns de agora ser parte desse grupo! Por favor, leia as {bot.get_channel(bot.RULE_CHANNEL).mention} e não seja um cuzão!"
        embed.set_image(url="https://i.pinimg.com/originals/70/37/d4/7037d478852af21357f038fac2d2e9f6.gif")
        embed.set_thumbnail(url=member.avatar.url)
        return embed
async def setup(bot):
    await bot.add_cog(OnMemberJoin())
