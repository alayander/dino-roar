"""
Dino Roar is a Discord bot to broadcast status updates for
Dino Jump, a project made by Spark Design Club.

The bot will fetch weekly updates from the team's Confluence page
and pass the data through an LLM for summarization.
"""

import os
import re
from datetime import datetime
from dotenv import load_dotenv
from discord import Intents
from discord.ext import commands
from dino_roar import confluence

# Load .env variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")


def main():
    """
    First entry point for Dino Roar.
    """
    # Initialize bot
    intents = Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="🦖 ", intents=intents)

    # Update command
    @bot.command(name="update")
    async def update(ctx, *, date_arg: str = None):

        date = re.match(r"^\d{2}/\d{2}/\d{4}$", date_arg)

        if date:
            date_obj = datetime.strptime(date.group(), "%m/%d/%Y")
            formatted_date = date_obj.strftime("%B %d, %Y")
            confluence.fetch_content(date=date.group())
            await ctx.send(f"**Dino Jump Status Update - {formatted_date}**")
        else:
            await ctx.send("Invalid `[date]` readback - expecting format mm/dd/yyyy")

    bot.run(DISCORD_TOKEN)
