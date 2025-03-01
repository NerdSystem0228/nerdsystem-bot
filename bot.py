from discord.ext import commands
import glob
import discord
import json
from dotenv import load_dotenv
from utils.logger import logger
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

# Sets bot intents
intents = discord.Intents(messages=True, message_content=True, guilds=True, members=True)

#Load bot data
class Runtime:
    fronters = {}
    
runtime = Runtime()    
MEMBERS=json.load(open("members.json"))
class Data(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    ) 
    TOKEN: str
    FRONT_CHANNEL: int
    RULE_CHANNEL: int
    WELCOME_CHANNEL: int
    BYE_CHANNEL: int
    MUSIC_CHANNEL: int
    SYSTEM_SERVER: int
    SYSTEM_ID: str
    API_KEY: str
    PREFIX: str
    APPLICATION_ID: str
    RCON_PASSWORD: str
    
data = Data() # type: ignore

#Creates bot instance
bot = commands.Bot(command_prefix=data.PREFIX,  # type: ignore
                         intents=intents,
                         application_id=data.APPLICATION_ID)

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
        for i in MEMBERS:
            if isinstance(id, str):
                continue
            if MEMBERS[i]["dcid"] == id:
                return i
            
        for i in MEMBERS:
            if isinstance(id, int):
                continue
            if id in MEMBERS[i]["spid"]:
                return i