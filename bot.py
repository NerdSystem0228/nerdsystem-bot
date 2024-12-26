from discord.ext import commands
import glob
import discord
import os
import json
from dotenv import load_dotenv
from utils.logger import logger

load_dotenv()

# Sets bot intents
intents = discord.Intents(messages=True, message_content=True, guilds=True, members=True)

#Creates bot instance
bot = commands.Bot(command_prefix=os.getenv("PREFIX"), 
                         intents=intents,
                         application_id=os.getenv("APPLICATION_ID"))

#Load bot data
bot.FRONT_CHANNEL=int(os.getenv("FRONT_CHANNEL"))
bot.RULE_CHANNEL=int(os.getenv("RULE_CHANNEL"))
bot.WELCOME_CHANNEL=int(os.getenv("WELCOME_CHANNEL"))
bot.BYE_CHANNEL=int(os.getenv("BYE_CHANNEL"))
bot.MUSIC_CHANNEL=int(os.getenv("MUSIC_CHANNEL"))
bot.SYSTEM_SERVER=int(os.getenv("SYSTEM_SERVER"))
bot.SYSTEM_ID=os.getenv("SYSTEM_ID")
bot.API_KEY=os.getenv("API_KEY")
bot.fronters={}
bot.members=json.load(open("members.json"))

async def load_cogs():
    for i in glob.glob("cogs/**/*.py", recursive=True):
            try:
                await bot.load_extension(f"{i.replace('/', '.')[:-3]}")
                logger.info(f"Loaded Extension: {i}")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                logger.error(
                    f"Failed to load extension {i}\n{exception}"
                )
                
def whois(id):
        for i in bot.members:
            if isinstance(id, str):
                continue
            if bot.members[i]["dcid"] == id:
                return i
            
        for i in bot.members:
            if isinstance(id, int):
                continue
            if id in bot.members[i]["spid"]:
                return i