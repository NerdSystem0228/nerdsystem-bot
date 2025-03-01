from discord.ext import commands
from bot import bot, data, MEMBERS
from discord import Embed
import datetime as dt

class OnFront(commands.Cog):
    def __init__(self):
        self.bot = bot 
        
    @commands.Cog.listener("on_front")
    async def on_front(self, member, color): 
        embed=self.create_front_embed(f"\n{member} está frontando!", color, bot.get_guild(data.SYSTEM_SERVER).get_member(int(MEMBERS[member]["dcid"])).avatar.url)
        await bot.get_channel(data.FRONT_CHANNEL).send(f"{bot.get_channel(data.FRONT_CHANNEL).guild.get_role(1296284550111957092).mention}", embed=embed)
    
    def create_front_embed(self, title, color, url):
        embed=Embed(title=title, color=color, timestamp=dt.datetime.now())
        embed.set_image(url=url)
        return embed
    
async def setup(bot):
    await bot.add_cog(OnFront())
