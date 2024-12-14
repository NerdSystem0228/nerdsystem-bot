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
