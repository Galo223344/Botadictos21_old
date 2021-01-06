import discord
import asyncio
import re
import json
from discord.ext import commands
from datetime import datetime, timedelta
from cogs.logs import logchannel
import random


# TODO: Comentar el codigo. Cambiar emojis por los del club de los 21


class Reactions(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    global giveaways
    giveaways = []
    global dict_gv
    dict_gv = {}

    with open('config.json', 'r') as f:
        configjson = json.load(f)
        global welcome_id
        welcome_id = int(configjson["welcome_id"])
        global welcome_channel_id
        welcome_channel_id = int(configjson["welcome_channel_id"])

    @commands.Cog.listener()
    async def on_ready(self):
        print ("Reacciones cog is ready")
        reaction_message = await self.bot.get_channel(welcome_channel_id).fetch_message(welcome_id)
        try:
            await reaction_message.add_reaction(emoji="<a:Thumbup:792171608323260416>")
        except:
            # print("fallo el poner la reaccion")
            pass
        # print(self.reaction_message)

    # @commands.Cog.listener()
    # async def on_reaction_add(self, reaction, user):
    #     pass
    #
    # @commands.Cog.listener()
    # async def on_reaction_remove(self, reaction, user):
    #     pass

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # print(payload)
        if payload.member.bot == True:
            return
        reaction_message = await self.bot.get_channel(welcome_channel_id).fetch_message(welcome_id)
        if payload.message_id == welcome_id:
            if str(payload.emoji) == "<a:Thumbup:792171608323260416>":
                role = discord.utils.get(payload.member.guild.roles, name="La People👤")
                await payload.member.add_roles(role)
                await reaction_message.remove_reaction(str(payload.emoji), payload.member)
                return
        for i in dict_gv:
            if i == payload.message_id:
                # print("Encontrado")
                if str(payload.emoji) == "<a:Tada:784983720226193428>":
                    # print("emoji correcto")
                    # print(i)
                    # print("impreso el valor de i")
                    if payload.member.id in dict_gv[i]:
                        # print("el usuario ya está ahí")
                        return
                    dict_gv[i].append(payload.member.id)
                    # print(dict_gv)

    # @commands.Cog.listener()
    # async def on_raw_reaction_remove(self, payload):
    #     print(payload)
    #     if payload.member.bot == True:
    #         print(bot)
    #         return
    #
    #     for i in dict_gv:
    #         print(i)
    #         if i in giveaways:
    #             print("encontrado remove")
    #             dict_gv[i].remove(payload.member.id)
    #             print(dict_gv)




    @commands.command(name="sorteo", aliases=["Sorteo","sort","Sort","gv","GV","giveaway","Giveaway"])
    @commands.has_permissions(manage_guild = True)
    async def giveaway(self, ctx, tiempo = None, cant_ganadores = None, nombre = None, *, desc = None):

        from cogs.logs import gvchannel


        if tiempo == None or cant_ganadores == None or nombre == None or desc == None:
            await ctx.send("Uso del comando: `!sorteo tiempo(1h o 1d) ganadores(Cantidad de ganadores) nombre(Nombre del sorteo) desc(Descripción del sorteo)`")
            return

        cant_ganadores = int(cant_ganadores)

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

        if minutos == 0 and horas == 0 and dias == 0:
            await ctx.send("Tiempo invalido")
            return

        tiempofinal = datetime.now().replace(microsecond=0,second=0) + timedelta(minutes=minutos,hours=horas,days=dias)
        tiempo_formateado = tiempofinal.strftime("%d/%m/%Y %H:%M")

        minutos = minutos * 60
        horas = horas * 3600
        dias = dias * 86400


        tiempodormir = minutos + horas + dias

        tadaa = self.bot.get_emoji(784983720226193428)

        embed=discord.Embed(title="Nuevo sorteo!", description=f"Creado por {ctx.message.author.mention}")
        embed.add_field(name=str(nombre), value=str(desc), inline=False)
        embed.add_field(name="Cantidad de ganadores", value=cant_ganadores, inline=False)
        embed.set_footer(text=f"Finaliza el {tiempo_formateado}, reacciona con 🎉 para entrar!")

        channel=self.bot.get_channel(gvchannel)
        message = await channel.send("@everyone Nuevo sorteo!", embed=embed)
        await message.add_reaction(emoji="<a:Tada:784983720226193428>")


        lchannel = self.bot.get_channel(logchannel)
        embed=discord.Embed(title="Nuevo sorteo", description=f"Creado por {ctx.message.author.mention}", color=0xff6600)
        embed.add_field(name=str(nombre), value=str(desc), inline=False)
        embed.add_field(name="Cantidad de ganadores: ", value=cant_ganadores, inline=False)
        embed.set_footer(text=f"Finaliza el {tiempo_formateado}.")
        await lchannel.send(embed=embed)


        global giveaways
        giveaways.append(message.id)
        global dict_gv
        dict_gv[message.id] = []

        # print(giveaways)
        # print(dict_gv)

        await asyncio.sleep(tiempodormir)

        if len(dict_gv[message.id]) == 0 or len(dict_gv[message.id]) < cant_ganadores:
            if len(dict_gv[message.id]) == 0:
                await ctx.send(f"\"{nombre}\": El sorteo finalizó sin ningun participante")
                del dict_gv[message.id]
                lchannel = self.bot.get_channel(logchannel)
                embed=discord.Embed(title=f"El sorteo \"{nombre}\" finalizó incorrectamente", description="No hubo participantes", color=0xff6600)

            else:
                await ctx.send(f"\"{nombre}\": No hubo suficientes participantes para la cantidad de premios disponibles. {ctx.message.author.mention}")
                del dict_gv[message.id]
                lchannel = self.bot.get_channel(logchannel)
                embed=discord.Embed(title=f"El sorteo \"{nombre}\" finalizó incorrectamente", description="No hubo suficientes participantes", color=0xff6600)

            await lchannel.send(embed=embed)

            del dict_gv[message.id]

            return

        ganadores = []

        while len(ganadores) < cant_ganadores:
            eleccion = random.choice(dict_gv[message.id])
            if eleccion not in ganadores:
                try:
                    eleccionn = ctx.guild.get_member(eleccion)
                    ganadores.append(eleccion)
                except:
                    continue


        for i in ganadores:
            ganador = ctx.guild.get_member(i)
            await ctx.send(f"Felicidades {ganador.mention} por ganar el sorteo \"{nombre}\"! {ctx.message.author.mention} se va a comunicar con vos brevemente")
            await ganador.send(f"**Felicidades, {ganador.mention}! 🎉 Acabas de ganar el sorteo \"{nombre}\". En las proximas horas, Gtadictos se va a comunicar con vos para entregarte el premio!**")



        del dict_gv[message.id]

        lchannel = self.bot.get_channel(logchannel)
        embed=discord.Embed(title=f"El sorteo {nombre} finalizó correctamente", description="Asegurense de contactar a los ganadores", color=0xff6600)
        await lchannel.send(embed=embed)


    # @commands.Cog.listener()
    # async def on_raw_reaction_remove(self, payload):
    #     pass

    @commands.command(name="init")
    @commands.has_permissions(manage_guild = True)
    async def init(self,ctx):
        embed=discord.Embed(title="", description=" ")
        embed.add_field(name="----------------", value="**Bienvenido, acá estan las reglas. Asegúrate de leerlas y aceptarlas antes de continuar**.", inline=False)
        embed.add_field(name="----------------", value="<a:Pin:784983430713835521> Antes de nada, les dejo el [link del canal](https://www.youtube.com/c/gtadictos21) de Gtadictos 21", inline=False)
        embed.add_field(name="#1", value="<a:Desaprobado:784983048508276787> **NO** insultar, discriminar o faltar el respeto entre los miembros/staff.", inline=False)
        embed.add_field(name="#2", value="<a:Desaprobado:784983048508276787> **NO** se permiten nombres/fotos obscenas. Queda a discreción del staff decidir que se considera como *", inline=False)
        embed.add_field(name="#3", value="<a:Desaprobado:784983048508276787> **NO** se permite el contenido +18/NSFW. Puede ser un meme cada tanto, pero no pongas una foto de tu prima.", inline=False)
        embed.add_field(name="#4", value="<a:Desaprobado:784983048508276787> **NO** spammear otros discords ajenos a esta comunidad.", inline=False)
        embed.add_field(name="#5", value="<a:Desaprobado:784983048508276787> **NO** spammear canales de YouTube/Twitch sin permiso!", inline=False)
        embed.add_field(name="#6", value="<a:Desaprobado:784983048508276787> **NO** se permite **comprar o vender NADA**, ya sea una bicicleta, un falcon o, un kilito de merca. ", inline=False)
        embed.add_field(name="#7", value="<a:Desaprobado:784983048508276787> **NO** se permite hacer flood, es decir, mensajes que puedan interrumpir una conversación o molestar como, por ejemplo, enviar demasiados mensajes en muy poco tiempo. ", inline=False)
        embed.add_field(name="#8", value="<a:Aprobado:784983108663246908> **USAR** los canales correspondientes, si vas a mandar un meme, mándalo a #🤡memes, etc.", inline=False)
        embed.add_field(name="#9", value="<a:Desaprobado:784983048508276787> Al entrar a un chat de voz, **NO GRITES NI SATURES EL MICROFONO**.", inline=False)
        embed.add_field(name="#10", value="<a:Alerta:784982996225884200> **SI USAS CHEATS/SCRIPTS, TE REGALAMOS UN VACACIONES PERMANENTES A UGANDA**.", inline=False)
        embed.add_field(name="#11", value="<a:Aprobado:784983108663246908> Para conseguir el rango de <@&750492534857400321> tenes que hablar con un <@&750492134695764059> o en su defecto con un <@&750491866570686535> y sin problemas, te lo van a dar!", inline=False)
        embed.add_field(name="#12", value="<a:Aprobado:784983108663246908> Ante cualquier duda o consulta, podes hablar con un <@&750492134695764059> o un <@&750491866570686535> y seguro te ayudan a solucionar el problema!", inline=False)
        embed.add_field(name="Algunos comandos de utilidad", value="_Son muy utiles!_", inline=False)
        embed.add_field(name="!ayuda", value="Este comando te muestra toda la lista de comandos", inline=False)
        embed.add_field(name="!nivel", value="Una vez que envíes algunos mensajes, usa este comando para conocer tu nivel.", inline=False)
        embed.add_field(name="!rank", value="Este comando muestra los 5 usuarios con más nivel en el servidor.", inline=False)
        embed.add_field(name="!botinfo", value="Este comando te muestra información extra acerca del bot, así como también, el código fuente!", inline=False)
        embed.add_field(name="----------------", value="<a:Aprobado:784983108663246908> Recordá que nosotros nos guiamos por los [términos y condiciones de discord](https://www.discord.com/terms) y por las [directivas de la comunidad](https://www.discord.com/guidelines).", inline=False)
        embed.set_footer(text="¡Para poder acceder a los demás canales, hace clic en el Emoji de abajo! \n\n Al hacer esto, aceptas las reglas y aceptas que de romperlas, podrías recibir las consecuencias correspondientes.")
        welcome_message = await ctx.send(embed=embed)
        await welcome_message.add_reaction(emoji="<a:Thumbup:792171608323260416>")

        global welcome_id
        welcome_id = welcome_message.id
        global welcome_channel_id
        welcome_channel_id = welcome_message.channel.id


        with open('config.json', 'r') as f:
            config = json.load(f)

        config["welcome_id"] = welcome_id
        config["welcome_channel_id"] = welcome_channel_id

        with open("config.json", "w") as outfile:
            json.dump(config, outfile)





def setup(bot):
    bot.add_cog(Reactions(bot))
