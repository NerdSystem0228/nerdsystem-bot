from discord.ext import commands

class OnReady(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot 
        
    @commands.Cog.listener("on_ready")
    async def on_ready(self): 
        self.bot.get_system_members()
        self.bot.show_all_members()

async def setup(bot):
    pass#await bot.add_cog(OnReady(bot))
