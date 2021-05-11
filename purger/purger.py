from discord.ext import commands
import discord

from core import checks
from core.models import PermissionLevel


def invalid_amount_embed():
    return discord.Embed(description="Invalid number provided, your command should look something like this: `["
                                     "?/!]purge 1<5`.",
                         colour=discord.Colour.red())


def no_permissions_embed():
    return discord.Embed(description="It looks like the bot doesn't have permission to delete messages, please verify "
                                     "this and try again.").\
        set_image(url="https://cdn.discordapp.com/attachments/806620866992406592/841588923791835156/unknown.png")


class PurgerCog(commands.Cog):
    def __init__(self):
        self.anon = False

    def cog_unload(self):
        pass

    @commands.command()
    # @checks.has_permissions(PermissionLevel.MODERATOR)
    async def purge(self, ctx: commands.Context, amount):
        try:
            assert int(amount) > 1
        except (AssertionError, ValueError):
            return await ctx.send(embed=invalid_amount_embed())

        try:
            await ctx.channel.purge(limit=int(amount) + 1)

        except discord.Forbidden:
            return await ctx.send(no_permissions_embed())

        # todo: better conversions
        embed = discord.Embed(description=f"Succesfully purged **{amount}** messages.",
                              colour=discord.Colour.green())

        if self.anon is False:
            embed.set_footer(text=ctx.author.name,
                             icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed, delete_after=5 if self.anon is False else 3)


def setup(bot):
    bot.add_cog(PurgerCog())
