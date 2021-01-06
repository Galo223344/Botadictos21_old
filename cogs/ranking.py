import discord
from discord.ext import commands
import json


class ranks(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print ("Ranking cog is ready")



    @commands.command(name="rank",aliases=["Rank","ranking","Ranking"])
    async def rank(self,ctx):
        with open('users.json', 'r') as f:
            data = json.load(f)

        leaderboard = get_top_experience(data)
        embed = discord.Embed(title='Tabla de posiciones', description='Ranking de experiencia de todos los usuarios', color=0xff5555)
        embed.add_field(name='**#1**', value=leaderboard[0], inline=False)
        embed.add_field(name='**#2**', value=leaderboard[1], inline=False)
        embed.add_field(name='**#3**', value=leaderboard[2], inline=False)
        embed.add_field(name='**#4**', value=leaderboard[3], inline=False)
        embed.add_field(name='**#5**', value=leaderboard[4], inline=False)
        await ctx.send(embed=embed)

def get_top_experience(data):
    users = []
    for k, v in data.items():
        users.append(ExperienceCount(k, v['experience']))
    return sorted(users, key=lambda x: x.experience, reverse=True)

class ExperienceCount:

    def __init__(self, user, experience):
        self.user = user
        self.experience = experience

    def __repr__(self):
        return f'<@{self.user}> con {self.experience} puntos de experiencia'

def setup(bot):
    bot.add_cog(ranks(bot))
