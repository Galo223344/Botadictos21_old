import discord
from discord.ext import commands
from discord.utils import get

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mping")
    async def ming(self, ctx):
            await ctx.send(f" Pong! {round(self.bot.latency * 1000)} ms")

def setup(bot):
    bot.add_cog(Misc(bot))
