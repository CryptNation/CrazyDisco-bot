# Welcome to CrazyDisco-dev
# I am looking into spotify support, but first I need to get youtube working and polished

# main.py
import asyncio
import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import youtube_dl

load_dotenv()
DISCORD_TOKEN = os.getenv("TOKEN")

intents = discord.Intents().all()
client = discord.Client(intents = intents)
bot = commands.Bot(command_prefix='dj!', intents=intents)

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': False,
    'nocheckcertificate': False,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __int__(self, source, *, data, volume =0.5):
        super().__init__(source, volume)
        self.data=data
        self.title = data.get('title')
        self.url = ''

    @classmethod
    async def from_url(cls, url, *, loop = None, stream = False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download = not stream))
        if 'entries' in data:
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

@bot.command(name='join')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
        await channel.connect()

@bot.command(name = 'play_song')
async def play(ctx,url):
    server = ctx.message.guild
    voice_channel = server.voice_client
    async with ctx.typing():
        filename = await YTDLSource.from_url(url, loop = bot.loop)
        voice_channel.play(discord.FFmpegPCMAudio(executable = "", source = filename))
    await ctx.send('**Now Playing:** {}'.format(filename))

@bot.command(name = 'pause')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.sent("My Audio system has already paused this file.")

@bot.command(name = 'resume')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("My Audio system is already playing. (If this is an error please report it to cpt.crypt)")

@bot.command(name='leave')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("Please understand that I am not in a voice chat..")

@bot.command(name='stop')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("I am not playing anything..")

if __name__ == "__main__":
    bot.run("TOKEN")


