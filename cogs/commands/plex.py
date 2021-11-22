"""
This File is for demonstrating and used as a template for future cogs.
"""

import logging

from discord.ext import commands
from utils import embeds
from utils.record import record_usage


# Enabling logs
log = logging.getLogger(__name__)


class PlexCog(commands.Cog):
    """PlexCog"""

    def __init__(self, bot):
        self.bot = bot
    
    @commands.before_invoke(record_usage)
    @commands.command(name="joinplex", aliases=['jp', 'join_plex'])
    async def join_plex_server(self, ctx, email: str = None):
        
        
        if not email:
            await ctx.send("You need to enter a valid email to join the plex!")
    
    
    

# The setup function below is necessary. Remember we give bot.add_cog() the name of the class in this case SimpleCog.
# When we load the cog, we use the name of the file.
def setup(bot) -> None:
    """Load the PlexCog cog."""
    bot.add_cog(PlexCog(bot))
    log.info("Cog loaded: PlexCog")
