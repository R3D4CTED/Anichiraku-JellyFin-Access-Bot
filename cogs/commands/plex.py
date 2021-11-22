"""
This File is for demonstrating and used as a template for future cogs.
"""

import logging

from discord.ext import commands
from discord.ext.commands.context import Context
from utils import embeds
import config
from utils.record import record_usage
from plexapi.server import PlexServer

plex_server = PlexServer(config.plex_url, config.plex_api_key)
# Enabling logs
log = logging.getLogger(__name__)


class PlexCog(commands.Cog):
    """PlexCog"""

    def __init__(self, bot):
        self.bot = bot
        
    @commands.is_owner()
    @commands.before_invoke(record_usage)
    @commands.command(name="addplex", aliases=['ap', 'add_to_plex'])
    async def add_to_plex_server(self, ctx, email: str = None):
        
        if not email:
            await ctx.send("You need to enter a valid email to join the plex!")
            
        try:
            plex_server.myPlexAccount().inviteFriend(user=email, server=plex_server,
                                                     sections=None,
                                                     allowSync=False,
                                                     allowCameraUpload=False,
                                                     allowChannels=False,
                                                     filterMovies=None,
                                                     filterTelevision=None,
                                                     filterMusic=None)
        except:
            log.error("Something went wrong when adding that user")
            return

        await ctx.send("Added user successfully!")
        
        
            
    @commands.before_invoke(record_usage)
    @commands.command(name="joinplex", aliases=['jp', 'join_plex'])
    async def join_plex_server(self, ctx: Context, email: str = None):
        
        guild = ctx.bot.get_guild(config.guild_id)
        plex_access_role = guild.get_role(config.plex_access_role)
        member = await guild.fetch_member(ctx.author.id)
        if member:
            if plex_access_role in member.roles:
                if not email:
                    await ctx.send("You need to enter a valid email to join the plex!")
                    return
                try:
                    plex_server.myPlexAccount().inviteFriend(user=email, server=plex_server,
                                                            sections=None,
                                                            allowSync=False,
                                                            allowCameraUpload=False,
                                                            allowChannels=False,
                                                            filterMovies=None,
                                                            filterTelevision=None,
                                                            filterMusic=None)
                except:
                    log.error("Something went wrong when adding that user")
                    await ctx.send("Something went wrong, please check your plex email ID.")
                    return

                await ctx.send("Added you successfully! Please check your email for the invite!")
            
            else:
                await ctx.send("Sorry, you cannot access the plex.")
                

    
    

# The setup function below is necessary. Remember we give bot.add_cog() the name of the class in this case SimpleCog.
# When we load the cog, we use the name of the file.
def setup(bot) -> None:
    """Load the PlexCog cog."""
    bot.add_cog(PlexCog(bot))
    log.info("Cog loaded: PlexCog")
