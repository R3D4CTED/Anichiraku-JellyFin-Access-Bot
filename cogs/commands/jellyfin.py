import logging

import discord
from discord.ext import commands
from discord.ext.commands.context import Context
import requests
import secrets

import config
from utils import embeds
from utils.record import record_usage


# Enabling logs
log = logging.getLogger(__name__)


class JellyFinCog(commands.Cog):
    """JellyFin Cog"""

    def __init__(self, bot):
        self.bot = bot
    
    @commands.is_owner()
    @commands.before_invoke(record_usage)
    @commands.command(name="addmember", aliases=['am', 'add_member'])
    async def add_to_jellyfin(self, ctx: Context, member: discord.Member, username: str = None):
        """ Manually add a member to the media centre. """
        
        if username is None:
            username = member.display_name
        
        password = secrets.token_urlsafe(16)
        response = requests.post(url=f"{config.jellyfin_base_url}/Users/New", 
                json={'Name': username, 'Password': password}, 
                headers={"X-Emby-Token": config.jellyfin_api_key})
        
        if not response.status_code == 200:
            await embeds.error_message(ctx=ctx, description="Something went wrong when creating a user.")
            return

        user_id = response.json()['Id']

        body = {
            "EnableAudioPlaybackTranscoding": False,
            "EnableVideoPlaybackTranscoding": False,
            "EnablePlaybackRemuxing": False,
            "EnableSyncTranscoding": False,
            "EnableMediaConversion": False
        }

        requests.post(url=f"{config.jellyfin_base_url}/Users/{user_id}/Policy", json=body, 
                    headers={"X-Emby-Token": config.jellyfin_api_key})        

        log.info(f"User created with user id: {user_id}.")

        try:
            embed = embeds.make_embed(title="Welcome to Anichiraku Media Beta!", color="gold")
            embed.description = f"Please go [here]({config.jellyfin_base_url}) to login."
            embed.add_field(name="Your credentials are:", value=f"\n**Username:** {username}\n**Password: **||{password}||")
            embed.set_image(url="https://media1.tenor.com/images/a9c114df59d644d43e1da6f3e7db66ca/tenor.gif?itemid=4838961")
            embed.set_thumbnail(url="https://raw.githubusercontent.com/jellyfin/jellyfin-ux/master/branding/NSIS/modern-install.png")
            embed.set_footer(text="⚠ Please change your password immediately after initial login.")
            
            channel = await member.create_dm()

            await channel.send(embed=embed)

        except:
            await embeds.error_message("The user has DMs closed.")
            channel = await ctx.author.create_dm()
            await channel.send(embed=embed)
            return
        
        await ctx.reply(f"Created a user for {member.mention} with the username: {username}.")

# The setup function below is necessary. Remember we give bot.add_cog() the name of the class in this case SimpleCog.
# When we load the cog, we use the name of the file.
def setup(bot) -> None:
    """Load the JellyFinCog cog."""
    bot.add_cog(JellyFinCog(bot))
    log.info("Cog loaded: JellyFinCog")
