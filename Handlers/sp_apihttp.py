import aiohttp
import datetime as dt
import time
from Handlers.logger import logger
import json
class SP_APIHttp():
    def __init__(self, bot) -> None:
        self.bot = bot
        self.headers={
            'Content-Type': 'application/json',
            "Authorization":f"{self.bot.API_KEY}"
            }
        
    async def get_member(self, id):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(f"https://api.apparyllis.com/v1/member/{self.bot.SYSTEM_ID}/{id}") as r:
                return await r.json()
     
    async def get_fronters(self):
        self.bot.fronters={}
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(f"https://api.apparyllis.com/v1/fronters/") as r:
                json= await r.json()
                for i in json:
                    self.bot.fronters[self.bot.whois(i["content"]["member"])]={"docid":f"{i['id']}", "front":i["content"]}
            
    async def set_alter_front(self, member):
        await self.get_fronters()
        for i in self.bot.fronters:
            if member in i:
                return {"alreadyonfront":True}
            
        async with aiohttp.ClientSession(headers=self.headers) as session: 
            json={
                "customStatus": "",
                "custom": False,
                "live": True,
                "startTime": round(time.time() * 1000),
                "endTime": round(time.time() * 1000),
                "member": self.bot.members[member]["spid"]
            }
            async with session.post(f"https://api.apparyllis.com/v1/frontHistory", json=json) as r:
                if r.status == 200:
                    logger.info(f"{member} was added to the front list successfully")
                    return True
                elif r.status == 401:
                    logger.error("Your API_KEY is invalid")
                    return False
                else:
                    logger.error(f"It was not possible to connect onto Simply Plural API, status code: {r.status}")
                    return False                
            
    async def remove_alter_front(self, member):
        await self.get_fronters()
        async with aiohttp.ClientSession(headers=self.headers) as session:
            try:
                json={
                    "customStatus": "",
                    "custom": True,
                    "live": False,
                    "startTime": self.bot.fronters[member]["front"]["startTime"],
                    "endTime": round(time.time() * 1000)
                }
                async with session.patch(f"https://api.apparyllis.com/v1/frontHistory/{self.bot.fronters[member]['docid']}", json=json) as r:
                    if r.status == 200:
                        logger.info(f"{member} was removed from front list successfully")
                        return True
                    elif r.status == 401:
                        logger.error("Your API_KEY is invalid")
                        return False
                    elif r.status == 404:
                        logger.error(f"Alter {member} isn't on front")
                        return {"notonfront":True}
                    else:
                        logger.error(f"It was not possible to connect onto Simply Plural API, status code: {r.status}")
                        return False
            except KeyError as e:
                logger.error(f"Alter {e} isn't on front")
                return {"notonfront":True}