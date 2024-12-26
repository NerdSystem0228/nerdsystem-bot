import discord
import os
import platform
from discord.ext import commands
from dotenv import load_dotenv
from utils.logger import logger
from bot import load_cogs, bot
from utils.sp_apihttp import get_fronters
from utils.sp_websocket import listen_forever
import asyncio

async def setup_hook():
    logger.info(f"Logged in as {bot.user.name}")
    logger.info(f"discord.py API Version: {discord.__version__}")
    logger.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    logger.info("------------------")
    await load_cogs()
    await get_fronters()
    asyncio.create_task(listen_forever(), name="sp_websocket")

bot.setup_hook = setup_hook

#Runs the bot
bot.run(os.getenv("TOKEN"))