from discord.ext import commands
import json
from Handlers.logger import logger
import asyncio
import socket
import asyncio
import websockets
import argparse

class SP_WebSocket():
    
    def __init__(self, bot, callback):
        # set some default values
        self.bot = bot
        self.reply_timeout = 10
        self.ping_timeout = 10
        self.sleep_time = 1
        self.callback = callback

    def on_front(self, member, color, live):
        self.bot.dispatch("front", member=member, color=color, live=live)
        
    def on_unfront(self, member, color, live):
        self.bot.dispatch("unfront", member=member, color=color, live=live)

    async def listen_forever(self):
        while True:
            logger.debug("Creating new connection...")
            try:
                async with websockets.connect("wss://api.apparyllis.com/v1/socket") as ws:
                    await ws.send(json.dumps({"op":"authenticate", "token":f"{self.bot.API_KEY}"}))
                    while True:
                        try:
                            reply = await asyncio.wait_for(ws.recv(), timeout=self.reply_timeout)
                        except (asyncio.TimeoutError, websockets.exceptions.ConnectionClosed):
                            try:
                                pong = await ws.ping()
                                await asyncio.wait_for(pong, timeout=self.ping_timeout)
                                logger.debug("Ping OK, keeping connection alive...")
                                continue
                            except:
                                logger.debug(
                                    "Ping error - retrying connection in {} sec (Ctrl-C to quit)".format(self.sleep_time))
                                await asyncio.sleep(self.sleep_time)
                                break
                        logger.debug("Server said > {}".format(reply))
                        if self.callback:
                            await self.callback(reply)
            except socket.gaierror:
                logger.debug(
                    "Socket error - retrying connection in {} sec (Ctrl-C to quit)".format(self.sleep_time))
                await asyncio.sleep(self.sleep_time)
                continue
            except websockets.exceptions.InvalidStatus:
                logger.debug("502 HTTP Code")
                logger.debug("Retrying connection in {} sec (Ctrl-C to quit)".format(self.sleep_time))
                await asyncio.sleep(self.sleep_time)
                continue
            except ConnectionRefusedError:
                logger.debug("Nobody seems to listen to this endpoint. Please check the URL.")
                logger.debug("Retrying connection in {} sec (Ctrl-C to quit)".format(self.sleep_time))
                await asyncio.sleep(self.sleep_time)
                continue
    
"""
    def __init__(self, bot) -> None:
        self.bot = bot
        self.wss="wss://api.apparyllis.com/v1/socket"
        self.is_running = False
        
    async def send_ping(self, ws):
        while self.is_running:
            await ws.send_str("ping")
            await asyncio.sleep(10)
        
    async def run(self):
        while True:
            logger.info("Loop started")
            async with aiohttp.ClientSession() as session:
                async with session.ws_connect(self.wss) as ws:
                    await ws.send_json({"op":"authenticate", "token":f"{self.bot.API_KEY}"})
                    async for msg in ws:
                        try:    
                            if msg.json()["msg"] ==  "Successfully authenticated":
                                logger.info("Succesfully connected to the WSS Simply Plural.")
                                self.is_running=True
                                send_ping=asyncio.create_task(self.send_ping(ws))
                            elif msg.json()["msg"] == "Authentication violation: Token is missing or invalid. Goodbye :)":
                                logger.info("Token is invalid")
                                await ws.close()
                                break
                            json_message=msg.json()   
                            if not "frontHistory" in json_message["target"]:
                                continue
                            
                            member=self.bot.whois(json_message["results"][0]["content"]["member"])
                            color=await self.bot.get_member_color(member)

                            if json_message["results"][0]["content"]["live"] and not self.bot.members[member]["pastlive"]:
                                self.bot.members[member]["pastlive"] = True
                                self.on_front(member, color, json_message["results"][0]["content"]["live"])
                            elif not json_message["results"][0]["content"]["live"] and self.bot.members[member]["pastlive"]:
                                self.bot.members[member]["pastlive"] = False
                                self.on_unfront(member, color, json_message["results"][0]["content"]["live"])
                        except json.decoder.JSONDecodeError as e:
                                if msg.data == "pong":
                                    logger.info("WebSocket connection was pong")
                                else:
                                    continue
                        except KeyError as e:
                            continue    
                    
            send_ping.cancel()
            logger.info("send_ping was cancelled")        
    """        
"""
            try:
                async with session.ws_connect(self.wss) as ws:
                    await ws.send_json({"op":"authenticate", "token":f"{self.bot.API_KEY}"})
                    async for msg in ws:
                        logger.info(msg.data)
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            json_message=json.loads(msg.data)
                            logger.info(json_message)   
                            
                            
                            except KeyError as e:
                                print(e)
                        elif msg.type == aiohttp.WSMsgType.ERROR:
                            break
            except aiohttp.client_exceptions.WSServerHandshakeError as e:
                logger.error(f"Connection closed: {e}")
                await self.run()
            except Exception as e:
                logger.error(f"Connection closed: {e}")"""
                
"""
class SPDispatcher(BaseDispatcher):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    def on_front(self, member, color, live):
        self.bot.dispatch("front", member=member, color=color, live=live)
        
    def on_unfront(self, member, color, live):
        self.bot.dispatch("unfront", member=member, color=color, live=live)
    
    async def on_connect(self):
        return await self.ws.send(json.dumps({"op":"authenticate", "token":f"{self.bot.API_KEY}"}))
    
    async def on_message(self, message: str):
        try:
            json_message=json.loads(message)
            if not "frontHistory" in json_message["target"]:
                return
            
            member=self.bot.whois(json_message["results"][0]["content"]["member"])
            color=await self.bot.get_member_color(member)
            
            if json_message["results"][0]["content"]["live"] and not self.bot.members[member]["pastlive"]:
                self.bot.members[member]["pastlive"] = True
                self.on_front(member, color, json_message["results"][0]["content"]["live"])
            elif not json_message["results"][0]["content"]["live"] and self.bot.members[member]["pastlive"]:
                self.bot.members[member]["pastlive"] = False
                self.on_unfront(member, color, json_message["results"][0]["content"]["live"])
        except json.decoder.JSONDecodeError as e:
            if "pong" in message:
                logger.info("WebSocket connection was pong")
            else:
                logger.error(e)
        except KeyError as e:
            print(e)
            
class SP_WebSocket(AsyncWebSocketApp):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__("wss://api.apparyllis.com/v1/socket", SPDispatcher(bot))

    async def send_ping(self):
        while self.is_running:
            await self.send("ping")
            await asyncio.sleep(10)
            
    async def run_forever(self):
        while True:
            logger.error(await self.connect())
            logger.info("Passou do connect")
            try:
                #send_ping=asyncio.create_task(self.send_ping())
                await self.ws_recv_loop()
                
            except asyncio.exceptions.CancelledError as ex:
                logger.error([type(ex), ex])
            
            except ConnectionClosedError as e:
                logger.error(f"Connection closed with error: {e}")
            
            await self.disconnect()
            logger.info("Passou do disconnect")
            
"""
