import discord
from discord.ext import commands
import json
import random

class Levels(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print ("Levels cog is ready")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open('users.json', 'r') as f:
            users = json.load(f)

        await update_data(self, users, member)

        with open('users.json', 'w') as f:
            json.dump(users, f, indent=4)


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot == False:
            with open('users.json', 'r') as f:
                users = json.load(f)

            await update_data(self, users, message.author)
            await add_experience(self, users, message.author, random.randint(1,2))
            await level_up(self, users, message.author, message)

            with open('users.json', 'w') as f:
                json.dump(users, f, indent=4)


    @commands.command(name="level", aliases=["Level","levels","Levels","nivel","Niveles"])
    async def level(self, ctx, member: discord.Member = None):
        if not member:
            id = ctx.message.author.id
            with open('users.json', 'r') as f:
                users = json.load(f)
            lvl = users[str(id)]['level']
            exp = users[str(id)]['experience']
            await ctx.send(f'Sos nivel {lvl} y tenés {exp} puntos de experiencia')
        else:
            id = member.id
            with open('users.json', 'r') as f:
                users = json.load(f)
            lvl = users[str(id)]['level']
            await ctx.send(f'{member} está en el nivel {lvl}!')


async def update_data(self, users, user):
        if not f'{user.id}' in users:
            users[f'{user.id}'] = {}
            users[f'{user.id}']['experience'] = 0
            users[f'{user.id}']['level'] = 1


async def add_experience(self, users, user, exp):
        users[f'{user.id}']['experience'] += exp


async def level_up(self, users, user, message):
        with open('levels.json', 'r') as g:
            levels = json.load(g)
        experience = users[f'{user.id}']['experience']
        lvl_start = users[f'{user.id}']['level']
        lvl_end = int(experience ** (1 / 4))
        if lvl_start < lvl_end:
            await(await message.channel.send(f'Felicidades {user.mention}, has subido al nivel {lvl_end}')).delete(delay=20)
            users[f'{user.id}']['level'] = lvl_end



def setup(bot):
    bot.add_cog(Levels(bot))
