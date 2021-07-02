import discord
import os
import math
from discord.ext import commands
from cogs.logs import logchannel
from pydactyl import PterodactylClient
from dotenv import load_dotenv

# Cargamos el .env con los tokens

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')



class Stats(commands.Cog):
    def __init__(self,bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print ("Stats. cog is ready")
    
    @commands.command(name='estadisticas', aliases=["stats","Stats","Estadisticas"])
    async def host(self,ctx):
        client = PterodactylClient('https://control.sparkedhost.us/', API_TOKEN).client
        my_servers = client.list_servers()
        servers = my_servers['data']['data']
        utils = []
        for server in servers:
            srv_id = str(server['attributes']['identifier'])
            utils.append(client.get_server_utilization(srv_id)['resources'])
        
    
        embed = discord.Embed(title="Estadisticas del servidor:", description="", color=ctx.author.colour) 
        for util in utils:
            embed.add_field(name="**CPU:**", value=f"{util['cpu_absolute']}%", inline=False)
            embed.add_field(name="**Memoria en uso:**", value=f"{math.ceil((util['memory_bytes']/1024)/1024)} MB", inline=False)
            embed.add_field(name="**Espacio en uso:**", value=f"{math.ceil((util['disk_bytes']/1024)/1024)} MB", inline=False)
            embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)    

def setup(bot):
    bot.add_cog(Stats(bot))