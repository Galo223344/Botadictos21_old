import discord
from discord.ext import commands

class Example(commands.Cog):
	def __init__(self,bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print("cog is online")

	@commands.command(name="cogping",aliases=["cping"])
	async def cping(self, ctx):
		await ctx.send(f"cog pong! {round(self.bot.latency * 1000)} ms")

def setup(bot):
	bot.add_cog(Example(bot))