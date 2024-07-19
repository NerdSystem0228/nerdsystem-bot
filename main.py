from discord.ext import commands, tasks
from discord.ext.commands import Context
import discord
import glob
import os
import platform
from dotenv import load_dotenv
from Handlers.logger import logger
from Handlers.sp_apihttp import SP_APIHttp
from Handlers.sp_websocket import SP_WebSocket
from Handlers.taskhandler import TaskHandler
import json
import asyncio
from Enums.member_color import MemberColor

intents = discord.Intents(messages=True, message_content=True, guilds=True, members=True)
load_dotenv()

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=os.getenv("PREFIX"), 
                         intents=intents,
                         application_id=os.getenv("APPLICATION_ID"),)
        self.FRONT_CHANNEL=int(os.getenv("FRONT_CHANNEL"))
        self.SYSTEM_SERVER=int(os.getenv("SYSTEM_SERVER"))
        self.SYSTEM_ID=os.getenv("SYSTEM_ID")
        self.API_KEY=os.getenv("API_KEY")
        self.APIHttp=SP_APIHttp(self)
        self.WebSocket=SP_WebSocket(self)
        self.taskhandler=TaskHandler()
        self.fronters={}
        self.members=json.load(open("members.json"))
        
    def whois(self, id):
        for i in self.members:
            if isinstance(id, str):
                continue
            if self.members[i]["dcid"] == id:
                return i
            
        for i in self.members:
            if isinstance(id, int):
                continue
            if id in self.members[i]["spid"]:
                return i
            
        return False
            
    def verifyMembersColor(self, member):
        if "Yuka" in member:
            return MemberColor.Yuka
        elif "Yuni" in member:
            return MemberColor.Yuni
        elif "Evenly" in member:
            return MemberColor.Evenly
        elif "Kiara" in member:
            return MemberColor.Kiara
        elif "Júlia" in member:
            return MemberColor.Julia
        elif "Sofia" in member:
            return MemberColor.Sofia
            
    def whatcolor(self, member):
        return self.verifyMembersColor(member)
                
    async def load_cogs(self):
        for i in glob.glob("cogs/**/*.py", recursive=True):
            try:
                await self.load_extension(f"{i.replace('/', '.')[:-3]}")
                logger.info(f"Loaded Extension: {i}")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                logger.error(
                    f"Failed to load extension {i}\n{exception}"
                )

    async def setup_hook(self):
        logger.info(f"Logged in as {self.user.name}")
        logger.info(f"discord.py API Version: {discord.__version__}")
        logger.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")
        logger.info("------------------")
        await self.load_cogs()
        asyncio.ensure_future(self.WebSocket.run())
        self.taskhandler.task_launcher(10, None, "pingsp", self.WebSocket.send_ping, self.wait_until_ready)


bot = Bot()
bot.run(os.getenv("TOKEN"))
    
    
    
