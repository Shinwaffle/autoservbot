import discord
from discord.ext import commands,tasks
import json
from time import sleep
import youtube_dl

with open("config.json") as f:
    config = json.load(f)
    token = config['token']
    prefix = config['prefix']

bot = commands.Bot(command_prefix=prefix)

@bot.command()
async def play(ctx, arg):
    vc = ctx.author.voice.channel
    vc = await vc.connect()

    ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    }

    # https://www.youtube.com/watch?v=3RS4b3QmaSw
    # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #    ydl.download({arg})
    # print(video)
    vc.play(discord.FFmpegPCMAudio(
        executable="/bin/ffmpeg",
        source="funny.mp4"
        )
    )
    while vc.is_playing():
        sleep(.1)
    await vc.disconnect()
    await ctx.send(arg)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
bot.run(token)
