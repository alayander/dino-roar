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


def extract_info(data, indent=0):
    """
    Recursively extract info from a dictionary into a Dicord formatted bullet list.

    Args:
        data (dict): Dictionary to be formatted in Discord bullet list style.
        indent (str): The level of indentation.

    Returns:
        str: Bullet list in Discord style.
    """
    bullet_list = ""
    bullet = "  " * indent + "- "

    for key, value in data.items():
        bullet_list += bullet + key + "\n"
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict):  # Check if item is a dictionary
                    bullet_list += extract_info(item, indent + 1)  # Recursive call
                else:
                    bullet_list += extract_info({item: None}, indent + 1)
        elif isinstance(value, dict):
            bullet_list += extract_info(value, indent + 1)

    return bullet_list


def dict_to_discord_message(data_dict: dict, formatted_date: str):
    """
    Converts a dictionary to formatted Discord message.

    Args:
        dict (dict): Dictionary to be formatted in Discord bullet list style.
        formatted_date (str): The date of the status update for message heading.

    Returns:
        str: Message to be sent via Discord bot.
    """
    heading = f"**Dino Jump Status Update - {formatted_date}**\n"
    body = extract_info(data_dict)
    print(f"{heading}{body}")
    return f"{heading}{body}"


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
            update_dict = confluence.fetch_content(date=date.group())
            await ctx.send(dict_to_discord_message(update_dict, formatted_date))
        else:
            await ctx.send("Invalid `[date]` readback - expecting format mm/dd/yyyy")

    bot.run(DISCORD_TOKEN)
