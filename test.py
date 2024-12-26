import aiohttp
import aiohttp.client_exceptions
import asyncio
from utils.logger import logger
from bot import get_member_color, whois

class SP_WebSocket():
    def __init__(self):
        pass
    

async def listen_forever():
    while True:    
        async with aiohttp.ClientSession() as session:
            try:
                async with session.ws_connect(url="wss://api.apparyllis.com/v1/socket", autoping=True) as ws:
                    await ws.send_json({"op":"authenticate", "token":"HLy7FsXdJAG6543IhFOi9nNBCmtXw8B+mJePyTnOE0BXKWiM8ot7XYXpcnyyd7yo"})
                    async for msg in ws:
                        json_message=msg.json()
                        
                        print(json_message)  
                    ws.close()
                    logger.info("Websocket connection closed, trying again...")
            except aiohttp.client_exceptions.ClientError as e:
                logger.info(f"Websocket falhou conexão: {e}")



ws = SP_WebSocket()

asyncio.run(listen_forever())