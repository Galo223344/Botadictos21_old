#TODO:
#   Cambiar el channelid de YTconfig.yml, poner logchannel. Cambiar emojis
#	musica, buscar y arreglar bugs


import os
import random
import json

from discord.ext import commands
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')


# logval = {"logchannel":0} #779861708339937330
# ignoreval = {"ignorelist":[]}

# logchannel = logval.get(logchannel)
global admin_ids
admin_ids = [503739646895718401, 388924384016072706]


@bot.event
async def on_ready():
    print(f'{bot.user.name} se ha conectado')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="a Gtadictos 21 | Usa !ayuda", url="https://youtube.com/c/gtadictos21"))


@bot.event
async def on_disconnect():
    print(f"{bot.user.name} se ha desconectado")

# @bot.event
# async def on_command_error(ctx, error):
    # if isinstance(error, commands.MissingRequiredArgument):
    #     await ctx.send('Faltan uno o más argumentos.')
    # if isinstance(error, commands.MissingPermissions):
    #     await ctx.send("Te faltan permisos para ejecutar este comando")
    # if isinstance(error, discord.ext.commands.errors.CommandNotFound):
    #     await ctx.send("Comando no encontrado")
    # if isinstance(error, discord.ext.commands.errors.NoPrivateMessage):
    #     await ctx.send("Este comando no se puede usar en mensajes privados")
    # if isinstance(error, discord.ext.commands.errors.UserNotFound):
    # 	await ctx.send("Usuario no encontrado")
    # print(error)

# @bot.event
# async def on_ready():
#     channel = bot.get_channel(780094535711719465)
#     Text= "Poner un \N{RUNNER} te da el rol y poner un \N{TABLE TENNIS PADDLE AND BALL} te lo saca"
#     Moji = await channel.send(Text)
#     await Moji.add_reaction(emoji="\N{RUNNER}")
#     await Moji.add_reaction(emoji="\N{TABLE TENNIS PADDLE AND BALL}")

# @bot.event
# async def on_reaction_add(reaction, user):
# 	channel = 780094535711719465
# 	if reaction.message.channel.id != channel:
# 		return
# 	if user == bot.user:
# 		return
# 	if str(reaction) == "\N{TABLE TENNIS PADDLE AND BALL}":
		# Role = discord.utils.get(user.guild.roles, name="test")
		# await user.add_roles(Role)
# 	elif str(reaction) == "\N{RUNNER}":
# 		Role = discord.utils.get(user.guild.roles, name="test")
# 		await user.remove_roles(Role)


################# COMANDO DE PRUEBA
# @bot.command(name="spam")
# async def spam(ctx,cantidad : int):
#     for i in range(cantidad):
#         await ctx.send(i+1)




##########################################################
#
# Cogs
#
##########################################################

# Cog load
@bot.command()
async def load(ctx, extension):
    if ctx.author.id not in admin_ids:
        return
    bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"cogs.{extension} ha sido cargada")

@bot.command()
async def unload(ctx, extension):
    if ctx.author.id not in admin_ids:
        return
    bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"cogs.{extension} ha sido descargada")

@bot.command()
async def reload(ctx,extension):
    if ctx.author.id not in admin_ids:
        return

    if extension == "all":
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                bot.unload_extension(f"cogs.{filename[:-3]}")

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                bot.load_extension(f"cogs.{filename[:-3]}")

        await ctx.send("Recargadas todas las extensiones")
        return

    bot.unload_extension(f"cogs.{extension}")
    bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"cogs.{extension} ha sido recargada")

# @bot.command()
# async def emojis(ctx):
#
#     for i in ctx.guild.emojis:
#         print("-----")
#         print (f"{i.name}   {i.id}")
#         print("-----")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(TOKEN)
