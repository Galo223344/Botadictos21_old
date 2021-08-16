import os
import random
import json

from discord.ext import commands
import discord
from dotenv import load_dotenv
import time
import asyncio

# Cargamos el .env con los tokens
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

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

@bot.command()
async def reload(ctx,extension):
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
        return
    # Descargamos y cargamos la extension especifica

    bot.unload_extension(f"cogs.{extension}")
    bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"La extension cogs.**{extension}** ha sido recargada")

# Cargamos todos los archivos adentro de cogs / como extensiones
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f"cogs.{filename[:-3]}")

# Corremos el bot
bot.run(TOKEN)
