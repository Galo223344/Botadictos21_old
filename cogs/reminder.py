import discord
import asyncio
import re
import os
from random import choice as rchoice
from string import ascii_letters
import json as js
from copy import deepcopy
from datetime import datetime, timedelta
from discord.ext import commands, tasks
from base64 import b64encode, b64decode

class Reminder(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    emg_guild = 750491736349999154
    emg_gen = 750491737524404224


    @commands.Cog.listener()
    async def on_ready(self):
        print ("Reminder cog is ready")
        self.checktiempo.start()


    async def codificar(self,texto):
        texto = texto.encode("utf-8")
        cod = b64encode(texto)
        return cod.decode("utf-8")

    async def decodificar(self,texto):
        texto = texto.encode("utf-8")
        decod = b64decode(texto)
        return decod.decode("utf-8")

    async def sacarTiempo(self,tiempo):
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
            return "Tiempo invalido"

        return [minutos,horas,dias]


    @commands.command(name="Remindme", aliases=["remindme","RemindMe","remindMe","recordarme","Recordarme"])
    async def reminder(self,ctx, tiempo=None, *, recordatorio=None):

        if tiempo == None:
            await ctx.send("Porfavor especifica un tiempo de la siguiente manera: `1m 1h 1d`")
            return
        if recordatorio == None:
            await ctx.send("Especifica un recordatorio!")
            return

        listaTiempo = await self.sacarTiempo(tiempo)

        if type(listaTiempo) is not list:
            await ctx.channel.send(listaTiempo)
            return

        minutos = listaTiempo[0]
        horas = listaTiempo[1]
        dias = listaTiempo[2]


        tiemporecordatorio = datetime.now().replace(microsecond=0,second=0) + timedelta(minutes=minutos,hours=horas,days=dias)
        pedido = datetime.now().replace(microsecond=0,second=0)

        pedido_formateado = pedido.strftime("%d/%m/%Y %H:%M")
        tiempo_formateado = tiemporecordatorio.strftime("%d/%m/%Y %H:%M")

        await ctx.send(f"Entendido, te voy a hacer acordar de \"{str(recordatorio)}\" el {tiempo_formateado} por mensaje privado.")

        recordatorio = await self.codificar(recordatorio)

        if ctx.channel.type is discord.ChannelType.private:
            lugarpedido = "Mensaje privado"
        else:
            lugarpedido = ctx.channel.name


        id_rec = ""
        for _ in range(25):
            id_rec = id_rec + rchoice(ascii_letters)


        with open("recordatorios.json", "r+") as archivo:
            recordatorios = js.load(archivo)

            recordatorios['usuarios'][id_rec] = {}
            recordatorios['usuarios'][id_rec]["id"] = str(ctx.author.id)
            recordatorios['usuarios'][id_rec]["mensaje"] = recordatorio
            recordatorios['usuarios'][id_rec]["tiempo"] = tiempo_formateado
            recordatorios['usuarios'][id_rec]["pedido"] = pedido_formateado
            recordatorios['usuarios'][id_rec]["lugar"] = lugarpedido
            if lugarpedido != "Mensaje privado":
                recordatorios['usuarios'][id_rec]["guild"] = ctx.guild.id

        with open("recordatorios.json", "w") as archivo:
            js.dump(recordatorios,archivo, indent=4)




    @tasks.loop(minutes=1)
    async def checktiempo(self):
        with open("recordatorios.json","r+") as reminders:
            recordatorios = js.load(reminders)
            # print(f"recordatorios pre: {recordatorios}")
            clon = deepcopy(recordatorios)

            for key,value in clon['usuarios'].items():
                usr_id = value["id"]
                mensaje = await self.decodificar(value["mensaje"])
                tiempo = value["tiempo"]
                tiempoPedido = value["pedido"]
                lugarPedido = value["lugar"]
                tiemporem =  datetime.strptime(tiempo,'%d/%m/%Y %H:%M')

                if tiemporem < datetime.now():
                    if lugarPedido != "Mensaje privado":
                        guild = value["guild"]
                        guild = await self.bot.fetch_guild(int(guild))
                        usuario = await guild.fetch_member(int(usr_id))
                    else:
                        usuario = await self.bot.fetch_user(int(usr_id))

                    embed=discord.Embed(title="Recordatorio!", color=0x008080)
                    embed.add_field(name="Hola! Te hablo para recordarte de lo siguiente:", value=f"\"{mensaje}\"", inline=False)
                    embed.set_footer(text=f"Recordatorio pedido el {tiempoPedido} en #{lugarPedido}")

                    try:
                        await usuario.send("Recordatorio!", embed=embed)
                    except:
                        guild = await self.bot.fetch_guild(emg_guild)
                        chan = await guild.fetch_channel(emg_gen)
                        await guild.chan.send(f"{usuario.mention} Intenté enviarte tu recordatorio por pivado pero falló!", embed=embed)

                    del recordatorios['usuarios'][key]

            # print(f"recordatorios post: {recordatorios}")
        with open("recordatorios.json","w") as reminders:
            js.dump(recordatorios,reminders, indent=4)




def setup(bot):
    bot.add_cog(Reminder(bot))
