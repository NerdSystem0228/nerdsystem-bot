import aiohttp
import discord
import time
from utils.logger import logger
from bot import whois, bot
headers={
            'Content-Type': 'application/json',
            "Authorization":f"{bot.API_KEY}"
        }
        
async def get_member(id):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f"https://api.apparyllis.com/v1/member/{bot.SYSTEM_ID}/{id}") as r:
            if r.status == 200:    
                json= await r.json()
                return json

async def get_member_color(member):
        content=await get_member(bot.members[member]["spid"])
        t=tuple(int(content["content"]["color"].lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
        return discord.Color.from_rgb(t[0], t[1], t[2]).value

async def get_fronters():
    bot.fronters={}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f"https://api.apparyllis.com/v1/fronters/") as r:
            json= await r.json()
            for i in json:
                bot.members[whois(i["content"]["member"])]["pastlive"] = True
                bot.fronters[whois(i["content"]["member"])]={"docid":f"{i['id']}", "front":i["content"]}
        
async def set_alter_front(member):
    await get_fronters()
    for i in bot.fronters:
        if member in i:
            return {"alreadyonfront":True}
        
    async with aiohttp.ClientSession(headers=headers) as session: 
        json={
            "customStatus": "",
            "custom": False,
            "live": True,
            "startTime": round(time.time() * 1000),
            "endTime": round(time.time() * 1000),
            "member": bot.members[member]["spid"]
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
    
async def remove_alter_front(member):
    await get_fronters()
    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            json={
                "customStatus": "",
                "custom": True,
                "live": False,
                "startTime": bot.fronters[member]["front"]["startTime"],
                "endTime": round(time.time() * 1000)
            }
            
            if bot.fronters[member]["front"]["live"]:        
                async with session.patch(f"https://api.apparyllis.com/v1/frontHistory/{bot.fronters[member]['docid']}", json=json) as r:
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
            else:
                logger.info(f"{member} isn't on front")
                return
        except KeyError as e:
            logger.error(f"Alter {e} isn't on front")
            return {"alreadyonfront":False}