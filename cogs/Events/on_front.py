from discord.ext import commands
from discord import Embed
import datetime as dt

class OnFront(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot 
        
    @commands.Cog.listener("on_front")
    async def on_front(self, member, colour, live): 
        if live == True and self.bot.members[member]["pastlive"] == False:
            self.bot.members[member]["pastlive"]=True
            embed=self.create_front_embed(f"{member} está frontando!", colour(), self.bot.get_guild(self.bot.SYSTEM_SERVER).get_member(int(self.bot.members[member]["dcid"])).avatar.url)
            await self.bot.get_channel(self.bot.FRONT_CHANNEL).send(embed=embed)
        
    def create_front_embed(self, tittle, colour, url):
        embed=Embed(title=tittle, colour=colour, timestamp=dt.datetime.now())
        embed.set_image(url=url)
        return embed
async def setup(bot):
    await bot.add_cog(OnFront(bot))
