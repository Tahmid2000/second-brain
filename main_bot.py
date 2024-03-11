import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from note import noteBot
from remindMe import remindMeBot

load_dotenv()
discord_bot_token = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

def check_not_exit(message, exit_function):
    if message.content.lower() == '!exit':
        exit_function()
    return True

def load_bots():
    noteBot.setup(bot)
    remindMeBot.setup(bot)

@bot.command()
async def exit(ctx):
    def authorize(m):
        print(m)
    await ctx.send('Exiting command')
    return


def run_bot():
    load_bots()
    bot.run(discord_bot_token)

run_bot()