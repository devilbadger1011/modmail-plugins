import discord
from discord.ext import commands

config = {
    "CHANNEL_ID": 123456789,
}


class CountingPlugin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self._latest = None

    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.bot.get_channel(id=config["CHANNEL_ID"])

        assert channel is not None

        c = await channel.fetch_message(id=channel.last_message_id)
        self._latest = c

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        await self.bot.process_commands(msg)

        if msg.channel.id != config["CHANNEL_ID"] or self._latest is None:
            return

        try:
            if int(msg.content) != int(self._latest.content) + 1:
                raise ValueError

            if msg.author.id == self._latest.author.id:
                raise ValueError

        except ValueError:
            await msg.delete()

        self._latest = msg


def setup(bot):
    bot.add_cog(CountingPlugin(bot))
