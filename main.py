import discord
from discord.ext import commands,tasks

import youtube_dl

import json, logging, subprocess

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

class StatusRetriever(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.printer.start()
        self.message = _list()

    def cog_unload(self):
        self.printer.cancel()

    @tasks.loop(seconds=60.0)
    async def printer(self):
        await self.bot.wait_until_ready()

        self.message = _list()
        print(self.message)
        if self.message == 'server is not online':
            await _set(False) 
        else:
            await _set(True)
        

async def _set(online: bool):
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game(
                                "server is online" if online else "server is offline"
                                ))
se:

def _list():
    if _ssh_command('/srv/minecraft/rcon list') == '255':
        return 'server is not online' 
    else:
        # the output of rcon is in bytes (b'') that is why we decode it
        # also, there is some random extra characters so we slice that off
         _ssh_command('/srv/minecraft/rcon list').decode('UTF-8')[:-5]
    

def _ssh_command(command):
    try:
        return subprocess.check_output(f"ssh shin@192.168.0.18 -p 30 {command}", shell=True)
    except Exception: 
        return '255'

@bot.command()
async def list(ctx):
    await ctx.send(_list())

@bot.command()
async def start(ctx):
    subprocess.call('sudo etherwake -i wlan0 00:0b:ab:95:8d:52', shell=True)
    await ctx.send("I'm on it!")

@bot.command()
async def reboot(ctx):
    _ssh_command('systemctl restart minecraft.service')
    await ctx.send("Restaring the server!")

@bot.command()
async def stop(ctx):
    _ssh_command('sudo shutdown now')    
    await ctx.send("Shutting down the server!")

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

bot.add_cog(StatusRetriever(bot))
bot.run(token)
