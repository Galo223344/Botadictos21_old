#TODO:
#   Por alguna razon ignorelist no funca en el servidor del club pero en el servidor de prueba funciona perfectamente bien.
#	musica, buscar y arreglar bugs


import os
import random
import json

from discord.ext import commands
import discord
from dotenv import load_dotenv

# Cargamos el .env con los tokens
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
# Ponemos todos los intents de dicord (Porque los necesitamos)
intents = discord.Intents.all()
# Configuramos la instancia del bot
bot = commands.Bot(command_prefix='!', intents=intents)
# Sacamos el comando de help predeterminado (Porque es malisimo)
bot.remove_command('help')

# Una manera primitiva de sacar el logchannel (OBSOLETA)

# logval = {"logchannel":0} #779861708339937330
# ignoreval = {"ignorelist":[]}
# logchannel = logval.get(logchannel)

# Id mio y de Gtadictos21 (Para configurar el bot y demás)
global admin_ids
admin_ids = [503739646895718401, 388924384016072706]


@bot.event
async def on_ready():
    print(f'{bot.user.name} se ha conectado')

    # Cambia la actividad del bot a "viendo a Gtadictos21", url no funciona por limitación de Discord
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="a Gtadictos 21 | Usa !ayuda", url="https://youtube.com/c/gtadictos21"))


@bot.event
async def on_disconnect():
    # Esto literalmente no tiene uso.
    print(f"{bot.user.name} se ha desconectado")


# Primera instacia de un errorhandler (OBSOLETO), nuevo errorhandler en errorhandler.py

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

# Primera instancia de lo que se convirtió reacciones.py

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

# Comando de spam para probar el comando "!purge", envía la cantidad de mensajes especificados

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
        # Si el que pidé el comando no está en la lista de admins lo ignoramos
        return
    # Carga la extensión especificada
    bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"cogs.{extension} ha sido cargada")

@bot.command()
async def unload(ctx, extension):
    if ctx.author.id not in admin_ids:
        # Si el que pidé el comando no está en la lista de admins lo ignoramos
        return
    # Descarga/apaga/deshabilita la extensión especidicada
    bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"cogs.{extension} ha sido descargada")

@bot.command()
async def reload(ctx,extension):
    if ctx.author.id not in admin_ids:
        # Si el que pidé el comando no está en la lista de admins lo ignoramos
        return

    if extension == "all":
        # Si se nos piden todas las extendiones (all) descargamos y cargamos todas las extensiones disponibles
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                bot.unload_extension(f"cogs.{filename[:-3]}")

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                bot.load_extension(f"cogs.{filename[:-3]}")

        await ctx.send("Recargadas todas las extensiones")
        return
    # Descargamos y cargamos la extension especifica

    bot.unload_extension(f"cogs.{extension}")
    bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"cogs.{extension} ha sido recargada")

# DEBUG: Imprime todos los emojis customizados de la guild en la consola. Especialmente útil para los emojis animados si no tenes discord nitro

# @bot.command()
# async def emojis(ctx):
#
#     for i in ctx.guild.emojis:
#         print("-----")
#         print (f"{i.name}   {i.id}")
#         print("-----")

# Cargamos todos los archivos adentro de cogs/ como extensiones
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f"cogs.{filename[:-3]}")

# Corremos el bot
bot.run(TOKEN)
