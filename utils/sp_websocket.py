import aiohttp
import aiohttp.client_exceptions
import asyncio
from utils.logger import logger
from bot import whois, bot, data, MEMBERS
from utils.sp_apihttp import get_member_color
        
def on_front(member, color):
    bot.dispatch("front", member=member, color=color)
    
def on_unfront(member, color):
    bot.dispatch("unfront", member=member, color=color)

async def ping(ws):
    while True:    
        await ws.send_str("ping")  
        await asyncio.sleep(10)  

async def listen_forever():
    while True:    
        async with aiohttp.ClientSession() as session:
            try:
                async with session.ws_connect(url="wss://api.apparyllis.com/v1/socket", autoping=True) as ws:
                    await ws.send_json({"op":"authenticate", "token":data.API_KEY})
                    asyncio.create_task(ping(ws))
                    async for msg in ws:
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            if msg.data == "pong":
                                logger.info("Websocket pong!")
                                continue
                        
                        json_message=msg.json()
                        
                        if not json_message:
                            continue 
                        
                        if json_message["msg"] == "Successfully authenticated":
                            logger.info("WebSocket connected and authenticated successfully!")
                            continue
                        elif json_message["msg"] == "Authentication violation: Token is missing or invalid. Goodbye :)":
                            logger.info("Simply Plural Authentication token invalid")
                            continue
                        
                        
                        if not "frontHistory" in json_message["target"]:
                            continue

                        member=whois(json_message["results"][0]["content"]["member"])
                        color=await get_member_color(member)

                        if json_message["results"][0]["content"]["live"] and not MEMBERS[member]["pastlive"]:
                            MEMBERS[member]["pastlive"] = True
                            on_front(member, color)
                        elif not json_message["results"][0]["content"]["live"] and MEMBERS[member]["pastlive"]:
                            MEMBERS[member]["pastlive"] = False
                            on_unfront(member, color)
                            
                
                    await ws.close()
                    logger.info("Websocket connection closed, trying again...")
            except aiohttp.client_exceptions.ClientError as e:
                logger.info(f"Websocket falhou conexão: {e}")
