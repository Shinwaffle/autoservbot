import discord
from discord.ext import commands,tasks
import json
from time import sleep
import youtube_dl
# above are just imports, also using from x import y.

with open("config.json") as f:
    config = json.load(f)
    token = config['token']
    prefix = config['prefix']
#context manager, open function, json, dictionary manipulation

bot = commands.Bot(command_prefix=prefix)
#some function stuff, kwarg

@bot.command()
#decorator
async def play(ctx, arg):
# asychronous function
    vc = ctx.author.voice.channel
    vc = await vc.connect()
    # await function

    ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    }
    # defining a dictionary with a list inside

    # https://www.youtube.com/watch?v=3RS4b3QmaSw
    # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #    ydl.download({arg})
    # print(video)
    vc.play(discord.FFmpegPCMAudio(
        executable="/bin/ffmpeg",
        source="funny.mp4"
        )
    )
    # kwargs

    while vc.is_playing():
        sleep(.1)
    await vc.disconnect()
    await ctx.send(arg)
    #some basic thread manipulation, await functions

@bot.event
#decorator
async def on_ready():
    print(f'We have logged in as {bot.user}')
    #f string
bot.run(token)
