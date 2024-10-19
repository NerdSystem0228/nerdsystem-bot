from discord.ext import commands
from discord import Embed
import discord
import datetime as dt
from Handlers.logger import logger
class OnMemberJoin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot 
        
    @commands.Cog.listener("on_member_join")
    async def on_front(self, member): 
        embed=self.create_welcome_embed(member)
        await self.bot.get_channel(self.bot.WELCOME_CHANNEL).send(member.mention, embed=embed)
    
    def create_welcome_embed(self, member):
        embed=Embed(title=f"Bem vindo ao {self.bot.get_guild(self.bot.SYSTEM_SERVER).name}!", color=discord.Color.blurple(), timestamp=dt.datetime.now())
        embed.description=f"Espero que goste de sua estadia nesse hospí- quero dizer, lugar com pessoas acolhedoras que tem mente aberta o suficiente para aceitar a existência de uma estrutura neural onde possibilita mais de uma consciência num mesmo cérebro, parabéns de agora ser parte desse grupo! Por favor, leia as {self.bot.get_channel(self.bot.RULE_CHANNEL).mention} e não seja um cuzão!"
        embed.set_image(url="https://i.pinimg.com/originals/70/37/d4/7037d478852af21357f038fac2d2e9f6.gif")
        embed.set_thumbnail(url=member.avatar.url)
        return embed
async def setup(bot):
    await bot.add_cog(OnMemberJoin(bot))
