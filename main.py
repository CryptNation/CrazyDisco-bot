# Welcome to CrazyDisco-dev 0.01 (The rebuild)

# main.py
import discord
from discord.ext import commands
import settings
import wavelink

logger = settings.logging.getLogger(__name__)

class MusicBot(commands.Cog):
    vc : wavelink.Player = None
    def __init__(self, bot):
        self.bot = bot
    async def setup(self):
        wavelink.NodePool.create_node(
            bot=self.bot,
            host="localhost",
            port=2333,
            password="TESTER"
        )

    @commands.command()
    async def join(self, ctx):
        channel =ctx.message.author.voice.channel
        if channel:
            self.vc = channel.connect(cls=wavelink.Player)
            await ctx.send(f"Connected to {channel.name}")
    @commands.command()
    async def add(self, ctx, *title str):

    @commands.command()
    async def play(self, ctx):





async def setup(bot):
    music_bot = MusicBot(bot)
    await bot.add_cog(music_bot)
    await music_bot.setup()
