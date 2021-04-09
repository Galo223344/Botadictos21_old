import discord
import asyncio
import re
from datetime import datetime, timedelta
from discord.ext import commands

class Reminder(commands.Cog):
    def __init__(self,bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print ("Reminder cog is ready")


    @commands.command(name="Remindme", aliases=["remindme","RemindMe","remindMe","recordarme","Recordarme"])
    async def reminder(self,ctx, tiempo=None, *, recordatorio=None):

        if tiempo == None:
            await ctx.send("Porfavor especifica un tiempo de la siguiente manera: `1m 1h 1d`")
            return
        if recordatorio == None:
            await ctx.send("Especifica un recordatorio!")
            return

        tiempo = tiempo.replace(" ","")

        listtiempo = re.findall('\d+|\D+', tiempo)

        if 'm' in listtiempo:
            indexm = listtiempo.index("m") -1
            # print("encontrada m")
        else:
            indexm = None

        if 'h' in listtiempo:
            indexh = listtiempo.index("h") - 1
            # print("encontrada h")
        else:
            indexh = None

        if 'd' in listtiempo:
            indexd = listtiempo.index("d") - 1
            # print("encontrada d")
        else:
            indexd = None

        ##########

        if indexm  is not None:
            minutos = int(listtiempo[indexm])
        else:
            minutos = 0

        if indexh is not None:
            horas = int(listtiempo[indexh])
        else:
            horas = 0

        if indexd is not None:
            dias = int(listtiempo[indexd])
        else:
            dias = 0


        if minutos <= 0 and horas <= 0 and dias <= 0:
            await ctx.send("Tiempo invalido")
            return

        tiemporecordatorio = datetime.now().replace(microsecond=0,second=0) + timedelta(minutes=minutos,hours=horas,days=dias)
        pedido = datetime.now().replace(microsecond=0,second=0)

        pedido_formateado = pedido.strftime("%d/%m/%Y %H:%M")
        tiempo_formateado = tiemporecordatorio.strftime("%d/%m/%Y %H:%M")

        await ctx.send(f"Entendido, te voy a hacer acordar de \"{str(recordatorio)}\" el {tiempo_formateado} por mensaje privado.")

        minutos = minutos * 60
        horas = horas * 3600
        dias = dias * 86400

        tiempodormir = minutos + horas + dias

        if ctx.channel.type is discord.ChannelType.private:
            lugarpedido = "Mensaje privado"
        else:
            lugarpedido = ctx.channel.name

        await asyncio.sleep(tiempodormir)

        embed=discord.Embed(title="Recordatorio!", color=0x008080)
        embed.add_field(name="Hola! Te hablo para recordarte de lo siguiente:", value=f"\"{recordatorio}\"", inline=False)
        embed.set_footer(text=f"Recordatorio pedido el {pedido_formateado} en #{lugarpedido}")

        await ctx.author.send("Recordatorio!", embed=embed)

def setup(bot):
    bot.add_cog(Reminder(bot))