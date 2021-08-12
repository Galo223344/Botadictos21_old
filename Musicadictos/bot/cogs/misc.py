import discord
from discord.ext import commands
from discord.utils import get

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mping")
    async def ming(self, ctx):
        ping = round(self.bot.latency * 1000)
        embed = discord.Embed(title=f":ping_pong: Ping Bot: {ping}ms", colour=ctx.author.colour)
        embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        inline=False
        await ctx.send(embed=embed)
        
def setup(bot):
    bot.add_cog(Misc(bot))
