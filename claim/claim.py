import discord
from discord.ext import commands


# from core import checks


def _success_embed(auth):
    return discord.Embed(description=f"This thread has been claimed by {auth.mention}",
                         colour=discord.Colour.green())


def _error_embed(dat):
    return discord.Embed(description=f"This thread has already been claimed by {dat.mention}",
                         colour=discord.Colour.red())


def _thread_not_claimed():
    return discord.Embed(description="This thread has not been claimed.",
                         colour=discord.Colour.blurple())


def _thread_not_yours():
    return discord.Embed(description="You may not unclaim this thread as it has been claimed by another user.",
                         colour=discord.Colour.red())


def _thread_success_deleted():
    return discord.Embed(description="This thread has been unclaimed successfully!",
                         colour=discord.Colour.green())


class ClaimPlugin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._temp_index = {}
        # todo: Add check for reply command

    @commands.command()
    # @checks.thread_only()
    async def claim(self, ctx):
        if ctx.channel in self._temp_index.keys():
            return await ctx.send(embed=_error_embed(dat=self._temp_index[ctx.channel]))

        self._temp_index[ctx.message.channel] = ctx.author

        c = await ctx.send(embed=_success_embed(auth=ctx.author))
        await c.pin(reason="Modmail thread claimed.")

    @commands.command()
    async def unclaim(self, ctx):
        if ctx.channel not in self._temp_index.keys():
            return await ctx.send(embed=_thread_not_claimed())

        if self._temp_index[ctx.channel] != ctx.author:
            return await ctx.send(_thread_not_yours())

        del self._temp_index[ctx.channel]
        await ctx.send(embed=_thread_success_deleted())


def setup(bot):
    bot.add_cog(ClaimPlugin(bot))
