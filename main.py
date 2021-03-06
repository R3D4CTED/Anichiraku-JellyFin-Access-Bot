import discord
from discord.ext import commands
import config
import glob

import __init__
import logging

log = logging.getLogger(__name__)

bot = commands.Bot(
    command_prefix=config.bot_prefix,
    intents=discord.Intents(messages=True, guilds=True, members=True, bans=True, reactions=True),
    case_insensitive=True)

@bot.event
async def on_ready():
    """Called when the client is done preparing the data received from Discord.
    For more information:
    https://discordpy.readthedocs.io/en/stable/api.html#discord.on_ready
    """
    log.info(f"Logged in as: {bot.user.name}#{bot.user.discriminator}")
    log.info(f"discord.py version: {discord.__version__}\n")

    # Adding in a activity message when the bot begins.
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.playing,
            name=f"Anime on Anichiraku Media."
        )
    )

if __name__ == '__main__':
    # Recursively loads in all the cogs in the folder named cogs.
    # Skips over any cogs that start with '__' or do not end with .py.
    for cog in glob.iglob("cogs/**/[!^_]*.py", recursive=True):
        try:
            if "\\" in cog:  # Fix pathing on Windows.
                bot.load_extension(cog.replace("\\", ".")[:-3])
            else:  # Fix pathing on Linux.
                bot.load_extension(cog.replace("/", ".")[:-3])
        except:
            continue

    # Finally, run the bot.
    bot.run(config.bot_token)

