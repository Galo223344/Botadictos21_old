import os
import random
import json
import math
import discord
import time
import asyncio

from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime
from pydactyl import PterodactylClient

# Abrimos el archivo config.json para saber el ID del logchannel
with open('config.json', 'r') as f:
    configjson = json.load(f)
    global logchannel
    logchannel = configjson["logchannel"]

# Cargamos el .env con los tokens
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
API_TOKEN = os.getenv('API_TOKEN')

# Forzamos la zona de tiempo a argentina
os.environ['TZ'] = 'America/Argentina/Buenos_Aires'
time.tzset()
print(time.strftime('%X %x %Z'))


# Ponemos todos los intents de discord (Porque los necesitamos)
intents = discord.Intents.all()
# Configuramos la instancia del bot
bot = commands.Bot(command_prefix='!', intents=intents)
# Sacamos el comando de help predeterminado (Porque es malisimo)
bot.remove_command('help')

# Id mio y de Gtadictos21 (Para configurar el bot y demás)
global admin_ids
admin_ids = [503739646895718401, 388924384016072706]

# Empieza un loop con distintos status
@bot.event    
async def status_task():
	while True:
		await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="a Gtadictos 21 | Usá !ayuda", url="https://youtube.com/c/gtadictos21"))
		await asyncio.sleep(10)
		guild = bot.get_guild(750491736349999154) # ID del servidor de Gtadictos21
		await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"a {len(guild.members)} usuarios | Usá !ayuda"))
		await asyncio.sleep(10)
		elegido = random.choice(guild.members)
		elegido = elegido.name
		await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"a {elegido} 👀 | Usá !ayuda"))
		await asyncio.sleep(10)

# Inicia el loop y avisa que el bot se conectó		
@bot.event      
async def on_ready():
    ...
    bot.loop.create_task(status_task())
    guild = bot.get_guild(750491736349999154) # ID del servidor de Gtadictos21	
    print(f'¡{bot.user.name} se ha conectado!¡Este servidor tiene {len(guild.members)} usuarios!')

    # Envia embed para avisar que el bot está activo, junto con algunos datos como uso de CPU, RAM, disco y ID de los operadores
    channel = bot.get_channel(853846800427384852) # ID del canal donde envia el mensaje	
    client = PterodactylClient('https://control.sparkedhost.us/', API_TOKEN).client
    srv_id = '17686b27'
    utils = []
    utils.append(client.get_server_utilization(srv_id)['resources'])

    for util in utils:
        embed=discord.Embed(title=f"¡{bot.user.name} se ha conectado!", description=f"¡Este servidor tiene {len(guild.members)} usuarios!", timestamp= datetime.now(), color=0x2bff00)
        embed.add_field(name="ID de los operadores:", value=f"{admin_ids}", inline=False)
        embed.add_field(name="**CPU:**", value=f"{util['cpu_absolute']}%/60%", inline=True)
        embed.add_field(name="**Memoria en uso:**", value=f"{math.ceil((util['memory_bytes']/1024)/1024)}MB/512MB", inline=True)
        embed.add_field(name="**Espacio en uso:**", value=f"{math.ceil((util['disk_bytes']/1024)/1024)}MB/10GB", inline=True)
        embed.set_thumbnail(url=bot.user.avatar_url)
    await channel.send(embed=embed)

print(os.path.exists('recordatorios.json'))

if not os.path.exists('recordatorios.json'):
    print("El archivo JSON de recordatorios no existe")
    with open("recordatorios.json", 'a') as outarch:
        print("Archivo creado supuestamente")
        
        objeto = {'usuarios':{}}
        print(objeto)
        print(outarch)
        json.dump(objeto, outarch, indent=4)
        print(outarch)
        # print(outarch.read())
        outarch.close()
else:
    print("El archivo JSON de recordatorios existe")


##########################################################
#
# Cogs
#
##########################################################

# Cog load
@bot.command()
async def load(ctx, extension):
    if ctx.author.id not in admin_ids:
        # Si el que pide el comando no es un Admin, aparece el error
        embed=discord.Embed(title="¡No tienes permisos para utilizar este comando!", description="Necesitas contar con el permiso `BOT_OPERATOR`", color=0xff0000)
        embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        return
    # Carga la extensión especificada
    bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"La extension cogs.**{extension}** ha sido cargada")

    channel=bot.get_channel(logchannel)
    embed=discord.Embed(title=f"Un operador ha cargado una extensión:", description=f"El operador {ctx.author.mention} ha cargado el cog **{extension}**", timestamp= datetime.now(), color=0xff7d00)
    embed.set_thumbnail(url=ctx.author.avatar_url)
    embed.set_footer(text=f"ID del usuario: {ctx.author.id}")
    await channel.send(embed=embed)

@bot.command()
async def unload(ctx, extension):
    if ctx.author.id not in admin_ids:
        # Si el que pide el comando no es un Admin, aparece el error
        embed=discord.Embed(title="¡No tienes permisos para utilizar este comando!", description="Necesitas contar con el permiso `BOT_OPERATOR`", color=0xff0000)
        embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        return
    # Descarga/apaga/deshabilita la extensión especidicada
    bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"La extension cogs.**{extension}** ha sido descargada")

    channel=bot.get_channel(logchannel)
    embed=discord.Embed(title=f"Un operador ha descargado una extensión:", description=f"El operador {ctx.author.mention} ha descargado el cog **{extension}**", timestamp= datetime.now(), color=0xff7d00)
    embed.set_thumbnail(url=ctx.author.avatar_url)
    embed.set_footer(text=f"ID del usuario: {ctx.author.id}")
    await channel.send(embed=embed)

@bot.command()
async def reload(ctx, extension):
    if ctx.author.id not in admin_ids:
        # Si el que pide el comando no es un Admin, aparece el error
        embed=discord.Embed(title="¡No tienes permisos para utilizar este comando!", description="Necesitas contar con el permiso `BOT_OPERATOR`", color=0xff0000)
        embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        return

    if extension == "all":
        # Si se nos piden todas las extensiones (all) descargamos y cargamos todas las extensiones disponibles
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                bot.unload_extension(f"cogs.{filename[:-3]}")

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                bot.load_extension(f"cogs.{filename[:-3]}")

        await ctx.send("¡Todas las extensiones han sido recargadas!")

        channel=bot.get_channel(logchannel)
        embed=discord.Embed(title=f"Un operador ha recargado todas las extensiones", description=f"El operador {ctx.author.mention} ha recargado todas las extensiones", timestamp= datetime.now(), color=0xff7d00)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text=f"ID del usuario: {ctx.author.id}") 
        await channel.send(embed=embed)
        return
    # Descargamos y cargamos la extension especifica
    bot.unload_extension(f"cogs.{extension}")
    bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"La extension cogs.**{extension}** ha sido recargada")

    channel=bot.get_channel(logchannel)
    embed=discord.Embed(title=f"Un operador ha recargado una extensión:", description=f"El operador {ctx.author.mention} ha recargado el cog **{extension}**", timestamp= datetime.now(), color=0xff7d00)
    embed.set_thumbnail(url=ctx.author.avatar_url)
    embed.set_footer(text=f"ID del usuario: {ctx.author.id}")
    await channel.send(embed=embed)

# Cargamos todos los archivos adentro de cogs / como extensiones
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f"cogs.{filename[:-3]}")

# Corremos el bot
bot.run(TOKEN)
