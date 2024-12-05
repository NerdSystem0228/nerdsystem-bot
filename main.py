from discord.ext import commands
import discord
import glob
import os
import platform
from dotenv import load_dotenv
from Handlers.logger import logger
from Handlers.sp_apihttp import SP_APIHttp
from Handlers.sp_websocket import SP_WebSocket
import json
import asyncio

intents = discord.Intents(messages=True, message_content=True, guilds=True, members=True)
load_dotenv()

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=os.getenv("PREFIX"), 
                         intents=intents,
                         application_id=os.getenv("APPLICATION_ID"),)
        self.FRONT_CHANNEL=int(os.getenv("FRONT_CHANNEL"))
        self.RULE_CHANNEL=int(os.getenv("RULE_CHANNEL"))
        self.WELCOME_CHANNEL=int(os.getenv("WELCOME_CHANNEL"))
        self.BYE_CHANNEL=int(os.getenv("BYE_CHANNEL"))
        self.MUSIC_CHANNEL=int(os.getenv("MUSIC_CHANNEL"))
        self.SYSTEM_SERVER=int(os.getenv("SYSTEM_SERVER"))
        self.SYSTEM_ID=os.getenv("SYSTEM_ID")
        self.API_KEY=os.getenv("API_KEY")
        self.counter = 0
        self.APIHttp=SP_APIHttp(self)
        self.fronters={}
        self.members=json.load(open("members.json"))
        self.SP_WEBSOCKET=SP_WebSocket(self, callback=self.callback_fn)
        
                
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

    async def get_member_color(self, member):
        content=await self.APIHttp.get_member(self.members[member]["spid"])
        t=tuple(int(content["content"]["color"].lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
        return discord.Color.from_rgb(t[0], t[1], t[2]).value
    
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

    def start_ws_client(self, client):
        asyncio.create_task(client.listen_forever())

    async def callback_fn(self, *args, **kwargs):
        json_str="".join(args)

        json_message=json.loads(json_str)
        try:
            if json_message["msg"] == "Successfully authenticated":
                logger.info("WebSocket connected and authenticated successfully!")
            elif json_message["msg"] == "Authentication violation: Token is missing or invalid. Goodbye :)":
                logger.info("Simply Plural Authentication token invalid")
                return
            
            if not "frontHistory" in json_message["target"]:
                return

            member=self.whois(json_message["results"][0]["content"]["member"])
            color=await self.get_member_color(member)

            if json_message["results"][0]["content"]["live"] and not self.members[member]["pastlive"]:
                self.members[member]["pastlive"] = True
                self.SP_WEBSOCKET.on_front(member, color, json_message["results"][0]["content"]["live"])
            elif not json_message["results"][0]["content"]["live"] and self.members[member]["pastlive"]:
                self.members[member]["pastlive"] = False
                self.SP_WEBSOCKET.on_unfront(member, color, json_message["results"][0]["content"]["live"])
        except json.decoder.JSONDecodeError as e:
            if args == "pong":
                logger.info("WebSocket connection was pong")
            else:
                return
        except KeyError as e:
            return    

    async def setup_hook(self):
        logger.info(f"Logged in as {self.user.name}")
        logger.info(f"discord.py API Version: {discord.__version__}")
        logger.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")
        logger.info("------------------")
        await self.load_cogs()
        await self.APIHttp.get_fronters()
        self.start_ws_client(self.SP_WEBSOCKET)



bot = Bot()
bot.run(os.getenv("TOKEN"))    
    
    
