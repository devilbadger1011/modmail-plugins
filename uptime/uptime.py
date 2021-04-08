import time
import psutil
import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel


def _format_time(seconds):
    return time.ctime(seconds)


class Uptime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self._load_time = time.time()
        self._boot_time = psutil.boot_time()
        self._bot_time = 0

    @commands.Cog.listener()
    async def on_ready(self):
        self._bot_time = time.time()

    @commands.command()
    @checks.has_permissions(PermissionLevel.REGULAR)
    async def uptime(self, ctx):
        embed = discord.Embed(title=f"{self.bot.user.name}'s Uptime Monitor",
                              colour=discord.Colour.blurple())
        embed.add_field(name="Cogs load time:", value=_format_time(self._load_time))
        embed.add_field(name="System boot time:", value=_format_time(self._boot_time))
        embed.add_field(name="Bot boot time:", value=_format_time(self._bot_time))

        embed.set_thumbnail(url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Uptime(bot))
