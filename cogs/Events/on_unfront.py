from discord.ext import commands
from bot import bot
from discord import Embed
import datetime as dt

class OnUnfront(commands.Cog):
    def __init__(self):
        pass
        
    @commands.Cog.listener("on_unfront")
    async def on_unfront(self, member, color):
        embed=self.create_front_embed(f"{member} saiu do front...", color, bot.get_guild(bot.SYSTEM_SERVER).get_member(bot.members[member]["dcid"]).avatar.url)
        await bot.get_channel(bot.FRONT_CHANNEL).send(f"{bot.get_channel(bot.FRONT_CHANNEL).guild.get_role(1296284550111957092).mention}", embed=embed)
    
    def create_front_embed(self, tittle, color, url):
        embed=Embed(title=tittle, color=color, timestamp=dt.datetime.now())
        embed.set_image(url=url)
        return embed
async def setup(bot):
    await bot.add_cog(OnUnfront())
