import os
import re
import discord
from datetime import datetime
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='🦖 ', intents=intents)

# Sample command
@bot.command(name='update')
async def update(ctx, *, input: str = None):

    date = re.match(r'^\d{2}/\d{2}/\d{4}$', input)

    if date:
        date_obj = datetime.strptime(date.group(), "%m/%d/%Y")
        formatted_date = date_obj.strftime("%B %d, %Y")
        await ctx.send(f"**Dino Jump Status Update - {formatted_date}**")
    else:
        await ctx.send(f"Invalid `[date]` readback - expecting format mm/dd/yyyy")

bot.run(DISCORD_TOKEN)