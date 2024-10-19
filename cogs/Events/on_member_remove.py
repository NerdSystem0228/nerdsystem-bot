from discord.ext import commands
from discord import Embed
import discord
import datetime as dt
from Handlers.logger import logger
class OnMemberRemove(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot 
        
    @commands.Cog.listener("on_member_remove")
    async def on_member_remove(self, member): 
        embed=self.create_bye_embed(member)
        await self.bot.get_channel(self.bot.BYE_CHANNEL).send(member.mention, embed=embed)

    def create_bye_embed(self, member):
        embed=Embed(title=f"Tchauzinho {member.display_name}!", color=discord.Color.red(), timestamp=dt.datetime.now())
        embed.description="""
Infelizmente um member saiu do 
nosso server... espero que num 
dia ele volte, ou não, vai que 
era um cuzão.
"""
        embed.set_image(url="https://media.discordapp.net/attachments/1297245011259162675/1297338078440198175/200w.gif?ex=67158fbd&is=67143e3d&hm=ff7676f0dd875162eaa7cfdbcd264eab24db34a8a58a253175f5003c80780138&=")
        embed.set_thumbnail(url=member.avatar.url)
        return embed
async def setup(bot):
    await bot.add_cog(OnMemberRemove(bot))
