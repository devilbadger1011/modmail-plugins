import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel


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


def _no_message_claimed():
    return discord.Embed(
        description="You cannot send a message to this thread's recipient as it is claimed by another user.",
        colour=discord.Colour.red())


def _thread_success_deleted():
    return discord.Embed(description="This thread has been unclaimed successfully!",
                         colour=discord.Colour.green())


class ClaimPlugin(commands.Cog):
    def __init__(self, bot, add_checks=True):
        self.bot = bot
        self._temp_index = {}
        if add_checks is False:
            return

        for cmd in [c for c in bot.commands if str(c) in ["reply", "areply"]]:
            @cmd.add_check
            async def _is_thread_owner(ctx):
                if ctx.channel not in self._temp_index.keys():
                    return True

                if self._temp_index[ctx.channel] != ctx.author:
                    await ctx.send(embed=_no_message_claimed())
                    return False

                return True

            break

    @commands.command()
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    @checks.thread_only()
    async def claim(self, ctx):
        if ctx.channel in self._temp_index.keys():
            return await ctx.send(embed=_error_embed(dat=self._temp_index[ctx.channel]))

        self._temp_index[ctx.message.channel] = ctx.author

        c = await ctx.send(embed=_success_embed(auth=ctx.author))
        await c.pin(reason="Modmail thread claimed.")

    @checks.has_permissions(PermissionLevel.SUPPORTER)
    @commands.command()
    async def unclaim(self, ctx):
        if ctx.channel not in self._temp_index.keys():
            return await ctx.send(embed=_thread_not_claimed())

        if self._temp_index[ctx.channel] != ctx.author:
            return await ctx.send(embed=_thread_not_yours())

        del self._temp_index[ctx.channel]
        await ctx.send(embed=_thread_success_deleted())


def setup(bot):
    bot.add_cog(ClaimPlugin(bot))
