import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix = '$', help_command=None)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.command()
async def setup(context):
    await context.send('Set up string!')

@client.command()
async def load(context, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(context, extension):
    client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@client.command()
async def abt(context):
    abt_text = "Hello! I am a bot designed to help with organizing parties through Discord!\n"\
                "I currently only have a few barebones functions regarding Parties, but there are more commands to be added later.\n"\
                "Start with $help to view the current commands, or $todo to see what's planned."
    await context.send(abt_text)

@client.command()
async def todo(context):
    todo_list = "Todo list:\n"\
                "- Add a voting system to sortie, swaplead, disband, and setObjective for players not leading parties.\n"\
                "- Implememnt a $kick for all party members based on votes.\n"\
                "- Add a timer delay for $sortie requests.\n"\
                "- Implement Events: Parties can join Events which will request sorties.\n"\
                "- Allow users to display party passwords and DM password to current party members.\n"\
                "- Implement proper player profiles so users can display max level and class/subclass.\n"\
                "- With player profiles, allow parties and events to have minimum level requirements.\n"\
                "- Persist data even when brought offline (will require Python I/O and logging user info)\n"\
                "- Allow for multiple parties/events to be joined for one user/party.\n"\
                "- Add more style to $help and $todo\n"\
                "- Reach through space-time and bring Matoi into NGS"
    await context.send(todo_list)

@client.command()
async def help(context):
    command_list = "List of Commands:\n"\
                "$help: What you're reading right now.\n"\
                "$abt: Small about page.\n"\
                "$git (NOT IMPLEMENTED): Github link for this bot's code.\n"\
                "$mkpt <party name>: Make a party with the given name.\n"\
                "$mypt: See your currently joined party.\n"\
                "$joinpt `<@User>`: Join a party the @'ed user is currently in.\n"\
                "$disband: Disbands party. (party leader only)\n"\
                "$leavept: Leave your current party.\n"\
                "$swaplead `<@User>`: Change the party leader to someone else in your party. (party leader only)\n"\
                "$setObjective <string>: Set the objective of your current party. (party leader only)\n"\
                "$sortie: Mission Start! (party leader only)\n"
    await context.send(command_list)
client.run(TOKEN)