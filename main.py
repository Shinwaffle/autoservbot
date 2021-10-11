import discord
from discord.ext import commands,tasks

import youtube_dl

import json, os, logging
logging.basicConfig(filename='example.log', level=logging.WARN)

with open("config.json") as f:
    config = json.load(f)
    token = config['token']
    prefix = config['prefix']


bot = commands.Bot(command_prefix=prefix)


@bot.check
async def has_mngsrv_role(ctx):
    for role in ctx.author.roles:
        if role.name == 'manage server':
            return True
    return False

# spaghetti mess lmao
# TODO: refactor this code. also, the try catch does not do what it's supposed to do 
# you have to take the output of os.popen(...).read() and interpret it

# ideas: create a cog to check server state
# depending on the state, check for amount of players etc
@bot.command()
async def list(ctx):
    await ctx.send(
        os.popen("ssh -p 30 shin@192.168.0.32 '/srv/minecraft/rcon list'").read()
        )

@bot.command()
async def start(ctx):
    await ctx.send(
        "I'm on it! \n" + os.popen("sudo etherwake -i eth0 00:0b:ab:95:8d:51").read()
        )

@bot.command()
async def reboot(ctx):
    await ctx.send(
        "Restaring the server!\n" + os.popen("ssh -p 30 shin@192.168.0.32 'systemctl restart minecraft.service'").read()        
        )

# this is supposed to be like "hey, the server isn't up so i can't shut it down"
# but the popen won't raise an exception if the ssh fails
@bot.command()
async def stop(ctx):
    try:
        await ctx.send(
            "Shutting down the server!\n" + os.popen("ssh -p 30 shin@192.168.0.32 'sudo shutdown now'").read()
            )
    except Exception as e:
        print('an exception happened! check logs please.')
        logging.warn(e)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
bot.run(token)
