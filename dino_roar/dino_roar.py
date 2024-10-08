import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Sample command
@bot.command(name='update')
async def ping(ctx):
    await ctx.send('Dino Jump!')

bot.run(DISCORD_TOKEN)