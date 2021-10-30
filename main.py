import os

import discord
from discord.ext import commands
from discord.interactions import Interaction
from dotenv.main import load_dotenv

from data.model.guild import Guild
from utils.config import cfg
from utils.context import BlooContext
from utils.database import db
from utils.permissions import permissions
from utils.logger import logger

initial_extensions = [
        "cogs.commands.info.stats",
        "cogs.commands.info.devices",
        "cogs.commands.info.userinfo",
        "cogs.commands.info.tags",
        "cogs.commands.info.jailbreaks",
    ]
intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.presences = True
mentions = discord.AllowedMentions(everyone=False, users=True, roles=False)


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # force the config object and database connection to be loaded
        if cfg and db and permissions:
            logger.info("Presetup phase completed! Connecting to Discord...")

    async def get_application_context(self, interaction: Interaction, *, cls=BlooContext) -> BlooContext:
        return await super().get_application_context(interaction, cls=cls)

bot = Bot(intents=intents, allowed_mentions=mentions)

@bot.event
async def on_ready():
    logger.info("""
            88          88                          
            88          88                          
            88          88                          
            88,dPPYba,  88  ,adPPYba,   ,adPPYba,   
            88P'    "8a 88 a8"     "8a a8"     "8a  
            88       d8 88 8b       d8 8b       d8  
            88b,   ,a8" 88 "8a,   ,a8" "8a,   ,a8"  
            8Y"Ybbd8"'  88  `"YbbdP"'   `"YbbdP"'   
                """)
    logger.info(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')


if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

bot.run(os.environ.get("BLOO_TOKEN"), reconnect=True)
