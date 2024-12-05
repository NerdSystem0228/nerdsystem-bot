from discord.ext import commands
from discord import Embed
import datetime as dt
from Handlers.logger import logger
import yt_dlp

class OnMusicSent(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot 
    
    def download_song(self, URL):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': '/home/ubuntu/hdd/share/songs/%(title)s.%(ext)s'
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.cookiejar.load("cookies.txt", ignore_discard=True, ignore_expires=True)
                ydl.download([URL])
        except yt_dlp.DownloadError as e:
            logger.error(f"Error downloading {URL}: {str(e)}")
    
    @commands.Cog.listener("on_message")
    async def on_music_sent(self, msg: str): 
        if msg.channel.id == self.bot.MUSIC_CHANNEL:
            test_list = ['.com', '.ru', '.net', '.org', '.info', '.biz', '.io', '.co', "https://", "http://"]
            link_matches = [ele for ele in test_list if(ele in msg.content)]
            if link_matches:
                self.download_song(msg.content)
             
    
    def create_front_embed(self, title, color, url):
        embed=Embed(title=title, color=color, timestamp=dt.datetime.now())
        embed.set_image(url=url)
        return embed
async def setup(bot):
    await bot.add_cog(OnMusicSent(bot))
