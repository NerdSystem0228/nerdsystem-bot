import websocket
from discord.ext import commands
from async_websocket_client.apps import AsyncWebSocketApp
from async_websocket_client.dispatchers import BaseDispatcher
import json
from Handlers.logger import logger
from Enums.member_color import MemberColor

class SPDispatcher(BaseDispatcher):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    def on_front(self, member, colour, live):
        self.bot.dispatch("front", member=member, colour=colour, live=live)
        
    def on_unfront(self, member, colour, live):
        self.bot.dispatch("unfront", member=member, colour=colour, live=live)
    
    async def on_connect(self):
        return await self.ws.send(json.dumps({"op":"authenticate", "token":f"{self.bot.API_KEY}"}))
    
    async def on_message(self, message: str):
        try:
            json_message=json.loads(message)
            if not "frontHistory" in json_message["target"]:
                return
            
            member=self.bot.whois(json_message["results"][0]["content"]["member"])
            colour=self.bot.whatcolor(self.bot.whois(json_message["results"][0]["content"]["member"]))
            if json_message["results"][0]["content"]["live"]:
                self.on_front(member, colour, json_message["results"][0]["content"]["live"])
            else:
                self.on_unfront(member, colour, json_message["results"][0]["content"]["live"])
            
        except json.decoder.JSONDecodeError as e:
            if "pong" in message:
                logger.info("WebSocket connection was pong")
            else:
                logger.error(e)
        except KeyError as e:
            logger.error(e)
        
class SP_WebSocket(AsyncWebSocketApp):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__("wss://api.apparyllis.com/v1/socket", SPDispatcher(bot))
    
    async def send_ping(self):
        return await self.send("ping")    