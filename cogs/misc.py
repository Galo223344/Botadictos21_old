import discord
from discord.ext import commands
from cogs.logs import logchannel
from unidecode import unidecode



# TODO: Comentar el codigo(?)


class Misc(commands.Cog):
    def __init__(self,bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print ("Misc. cog is ready")


    # Youtube

    @commands.command(name='youtube', help="Link de mi canal de youtube", aliases=["Youtube","YT","yt","Yt"])
    async def youtube(self,ctx):
        await ctx.send("Acá está el link! https://www.youtube.com/c/gtadictos21")

    @commands.command(name="status")
    async def status(self,ctx):
        await ctx.send("Status de los servidores en https://status.gtadictos21.com/")

    # Invitacion

    @commands.command(name='invitacion', help="Link de la invitacion para el server de Discord", aliases=["Invitacion","invitación","Invitación","invite","Invite","inv"])
    async def invitec(self,ctx):
        # if ctx.channel.type is discord.ChannelType.private:
        #     await ctx.send("Comando no disponible en mensajes privados")
        #     return
        # link = await ctx.channel.create_invite(max_age = 300)
        await ctx.send(f"Espero que invites a tus amigos ;) \n https://Gtadictos21.com/discord")

    # El baile del troleo

    @commands.command(name='nopruebesestecomando', help="No lo hagas", aliases=["Nopruebesestecomando","Nopurebesestecomando","nopurebesestecomando"])
    async def invitacion(self,ctx):
        if ctx.channel.type is discord.ChannelType.private:
            return
        link = await ctx.channel.create_invite(max_age = 10000, max_uses=1,reason="baile del troleo")
        await ctx.author.send("Troleado " + str(link))
        await ctx.guild.kick(ctx.author)

        channel = self.bot.get_channel(logchannel)
        embed=discord.Embed(title="Alguien fue troleado", color=0xff6600)
        embed.add_field(name=f"{ctx.author} usó !nopruebesestecomando", value="xdxdxdxdxdxdxd", inline=True)

        await channel.send(embed=embed)
        # print(f"en teoría {ctx.author} fue kickeado")

    # Bot info

    @commands.command(name="botinfo", help="Muestra información del bot", aliases=["Botinfo","BotInfo","infobot","Infobot"])
    async def botinfo(self,ctx):
        embed=discord.Embed(title="Haz click para ver el codigo fuente", url="https://github.com/Galo223344/Botdictos21/", description="", color=0x2cdca3)
        embed.add_field(name="Botdictos por", value="<@388924384016072706>", inline=True)
        embed.add_field(name="Musicadictos por", value="<@503739646895718401>", inline=True)
        embed.add_field(name="Para el servidor", value="**El Club de los 21\'s**", inline=True)
        embed.add_field(name="Hosteado en", value="SparkedHost.us", inline=True)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

    # Ayuda

    @commands.command(name="ayuda", help="Te envía ayuda", aliases=["Ayuda","Help","help"])
    async def ayuda(self,ctx, argum = None):

        if argum is None:
            embed=discord.Embed(title="Ayuda", description="Comandos disponibles:", color=0x80ff00)
            embed.add_field(name="!Ayuda", value="Te envia este mensaje!", inline=False)
            embed.add_field(name="!Youtube", value="El link para mi canal de youtube!", inline=False)
            embed.add_field(name="!Invitacion", value="Te da un link de invitación para el servidor de discord!", inline=False)
            embed.add_field(name="!Nopruebesestecomando", value="No lo hagas!", inline=False)
            embed.add_field(name="!Botinfo", value="Te envia información acerca del bot", inline=False)
            embed.add_field(name="!Userinfo", value="Te da información de vos mismo o de alguien más!", inline=False)
            embed.add_field(name="!Sugerencia", value="Usar en privado. Te permite enviar una sugerencia!", inline=False)
            embed.add_field(name="!Avatar", value="Te envía una foto de tu avatar actual", inline=False)
            embed.add_field(name="!Remindme/Recuerdame", value="(Uso: !recuerdame 1m/1h/1d cosa a recordar).\nTe envía un mensaje privado después del tiempo especificado con el contenido a recordar", inline=False)
            embed.add_field(name="!Reaccion/React [palabras]", value="Reacciona al mensaje que respondiste con las palabras que mandaste\nNo usar Ñ, mensajes de más de 15 cáracteres o letras repetidas.", inline=False)
            await ctx.send(embed=embed)

            return

        if (argum.lower() == "mod" or argum.lower() == "moderacion") and ctx.author.guild_permissions.kick_members:
            embed=discord.Embed(title="Comandos de moderación", color=0xffff00)
            embed.add_field(name="!mute/silenciar (usuario)", value="Mutea al usuario. Permisos requeridos: Manejar roles", inline=False)
            embed.add_field(name="!tempmute (usuario) (tiempo {*m *h *d})", value="Mutea al usuario temporalmente. Permisos requeridos: Manejar roles", inline=False)
            embed.add_field(name="!unmute/dessilenciar (usuario)", value="Desmutea al usuario. Permisos requeridos: Manejar roles", inline=False)
            embed.add_field(name="!kick/expulsar (usuario)", value="Expulsa a el usuario especificado. Permisos requeridos: Kickear usuarios", inline=False)
            embed.add_field(name="!ban (usuario) (razón)", value="Banea a el usuario indefinidamente. Permisos requeridos: Banear usuarios", inline=False)
            embed.add_field(name="!tempban (usuario) (tiempo) (razón)", value="Banea a el usuario y lo desbanea una vez expira el tiempo especificado. IMPORTANTE, al usar tiempos complejos tales como '1h 30m' es necesario poner el tiempo entre comillas. Permisos requerios: Banear ususarios", inline=False)
            embed.add_field(name="!unban/desbanear (usuario con tag)", value="Desbanea a el usuario. Permisos requerios: Banear usuarios", inline=False)
            embed.add_field(name="!purge (cantidad)", value="Elimina la cantidad de mensajes especificados con un limite de 500 mensajes. Permisos requeridos: Manejar server", inline=False)
            await ctx.send(embed=embed)

        elif argum.lower() == "admin" and ctx.author.guild_permissions.manage_guild:
            embed=discord.Embed(title="Comandos de administación", color=0x008000)
            embed.add_field(name="!logchannel", value="Se van a enviar todos los logs a este canal", inline=False)
            embed.add_field(name="!init", value="Envía mensaje de bienvenida y comienza a escuchar reacciones", inline=False)
            embed.add_field(name="!gvchannel", value="Se van a enviar todos los sorteos a este canal", inline=False)
            embed.add_field(name="!ignore", value="Los logs ignoraran este canal", inline=False)
            embed.add_field(name="!ignorelist", value="envía una lista de todos los canales en la ignorelist", inline=False)
            embed.add_field(name="!sugchannel", value="Se envian las sugerencias a este canal", inline=False)
            embed.add_field(name="!mc comando \"comando\"", value="Envia comando al server de minecraft", inline=False)
            embed.add_field(name="!mc start", value="Inicia el server de minecraft", inline=False)
            embed.add_field(name="!mc restart", value="Reinicia el server de minecraft", inline=False)
            embed.add_field(name="!mc stop", value="Para el server de minecraft", inline=False)

            await ctx.send(embed=embed)

        elif argum.lower() == "música" or argum.lower() == "musica" or argum.lower() == "music":
            embed=discord.Embed(title="Ayuda de música", description="Comandos disponibles:", color=0xC70039)
            embed.add_field(name="!Conectar", value="Conecta Musicadictos a tu canal actual", inline=False)
            embed.add_field(name="!Desconectar", value="Desconecta Musicadictos de tu canal actual", inline=False)
            embed.add_field(name="!Play [Link o búsqueda de YT]", value="Reproduce la canción/lista especificada", inline=False)
            embed.add_field(name="!Pausa", value="Pausa la canción actual", inline=False)
            embed.add_field(name="!Stop", value="Para la música", inline=False)
            embed.add_field(name="!Skip", value="Saltea la canción actual", inline=False)
            embed.add_field(name="!Anterior", value="Reproduce la canción anterior", inline=False)
            embed.add_field(name="!Repetir", value="Activa/desactiva el modo repetición", inline=False)
            embed.add_field(name="!Cola", value="Te muestra la cola de música actual", inline=False)
            await ctx.send(embed=embed)



    # Ping

    @commands.command(name="ping")
    async def ping(self, ctx):
            await ctx.send(f" Pong! {round(self.bot.latency * 1000)} ms")


    # Sugerencia


    @commands.command(name="sugerencia", help="Envía tu sugerencia!", aliases=["Sugerencia","Sug","sug"])
    async def sugerencia(self,ctx, *, suge=None):

        from cogs.logs import sugchannel

        if ctx.channel.type is not discord.ChannelType.private:
            await ctx.send("Escribime la sugerencia al privado!")
            await ctx.author.send("Puedes enviar tu sugerencia por aquí.")
            return
        if suge == None:
            await ctx.send("La sugerencia no puede estar vacía!")
            return
        suge = str(suge)
        channel=self.bot.get_channel(sugchannel)
        embed=discord.Embed(color=0x8080ff)
        embed.add_field(name=f"{ctx.author} ha sugerido lo siguiente", value=f"\"{suge}\"", inline=True)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        mnsj = await channel.send(embed=embed)
        await mnsj.add_reaction("✅")
        await mnsj.add_reaction("❌")
        await ctx.send("Sugerencia enviada!")

    # userinfo

    @commands.command(name="userinfo", aliases=["Userinfo","infouser","Infouser"])
    async def userinfo(self,ctx, member: discord.Member=None):
        if member == None:
            member = ctx.author
        pingyo = False
        if member.id == 388924384016072706:
            pingyo = True

        roles = [role for role in member.roles]
        esunbot = "No"

        if member.bot:
            esunbot = "Si"

        embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)
        embed.set_author(name=f"Info de usuario - {member}")

        embed.set_footer(text=f"Pedido por - {ctx.author}", icon_url=ctx.author.avatar_url)

        embed.add_field(name="ID:", value=member.id)
        embed.add_field(name="Nombre:", value=member.display_name)

        embed.add_field(name="Cuenta creada el:", value=member.created_at.strftime("%a, %#d, %B, %Y, %I:%M %p UTC"))
        embed.add_field(name="Unido el:", value=member.joined_at.strftime("%a, %#d, %B, %Y, %I:%M %p UTC"))

        embed.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]))
        embed.add_field(name="¿Es un bot?", value=f"{esunbot}")

        embed.set_thumbnail(url=member.avatar_url)


        if pingyo:
            embed.add_field(name="¿Es mi creador?", value="**Si**")


        await ctx.send(embed=embed)

    #Avatar

    @commands.command(name="avatar", aliases=["Avatar"])
    async def avatar(self, ctx, member: discord.Member=None):
        if member == None:
            member = ctx.author

        await ctx.send(member.avatar_url)

    @commands.command(name='host', aliases=["Host","hosting","Hosting"])
    async def host(self,ctx):
        await ctx.send("Powered by https://billing.SparkedHost.com/aff.php?aff=1125 \n¿Querés tener tu propio servidor? ¡Usá el código \"Gtadictos21\" y obtené un 15\% de descuento!")

    @commands.command(name="eco", aliases=["echo","Echo","Eco"])
    @commands.has_permissions(kick_members = True)
    async def eco(self,ctx,canal:discord.TextChannel,*,mensaje:str):
        embed=discord.Embed(title=mensaje,value="",colour=ctx.author.color)
        await canal.send(embed=embed)




    @commands.command(name="reglas")
    @commands.has_permissions(manage_guild = True)
    async def reglas(self,ctx):
        embed=discord.Embed(title="", description=" ")
        embed.add_field(name="----------------", value="**Reglas\nSi no las recordas, aca las podes leer :)**.", inline=False)
        embed.add_field(name="----------------", value="<a:Pin:784983430713835521> Antes de nada, les dejo el [link del canal](https://www.youtube.com/c/gtadictos21) de Gtadictos 21", inline=False)
        embed.add_field(name="#1", value="<a:Desaprobado:784983048508276787> **NO** insultar, discriminar o faltar el respeto entre los miembros/staff.", inline=False)
        embed.add_field(name="#2", value="<a:Desaprobado:784983048508276787> **NO** se permiten nombres/fotos obscenas. Queda a discreción del staff decidir que se considera como obsceno.", inline=False)
        embed.add_field(name="#3", value="<a:Desaprobado:784983048508276787> **NO** se permite el contenido +18/NSFW. Puede ser un meme cada tanto, pero no pongas una foto de tu prima.", inline=False)
        embed.add_field(name="#4", value="<a:Desaprobado:784983048508276787> **NO** spammear otros discords ajenos a esta comunidad.", inline=False)
        embed.add_field(name="#5", value="<a:Desaprobado:784983048508276787> **NO** spammear canales de YouTube/Twitch sin permiso!", inline=False)
        embed.add_field(name="#6", value="<a:Desaprobado:784983048508276787> **NO** se permite **comprar o vender NADA**, ya sea una bicicleta, un falcon o, un kilito de merca. ", inline=False)
        embed.add_field(name="#7", value="<a:Desaprobado:784983048508276787> **NO** se permite hacer flood, es decir, mensajes que puedan interrumpir una conversación o molestar como, por ejemplo, enviar demasiados mensajes en muy poco tiempo. ", inline=False)
        embed.add_field(name="#8", value="<a:Aprobado:784983108663246908> **USAR** los canales correspondientes, si vas a mandar un meme, mándalo a <#750496337916592199>, etc.", inline=False)
        embed.add_field(name="#9", value="<a:Desaprobado:784983048508276787> Al entrar a un chat de voz, **NO GRITES NI SATURES EL MICROFONO**.", inline=False)
        embed.add_field(name="#10", value="<a:Alerta:784982996225884200> **SI USAS CHEATS/SCRIPTS, TE REGALAMOS UNAS VACACIONES PERMANENTES A UGANDA**.", inline=False)
        embed.add_field(name="#11", value="<a:Aprobado:784983108663246908> Para conseguir el rango de <@&750492534857400321> tenes que hablar con un <@&750492134695764059> o en su defecto con un <@&750491866570686535> y sin problemas, te lo van a dar!", inline=False)
        embed.add_field(name="#12", value="<a:Aprobado:784983108663246908> Ante cualquier duda o consulta, podes hablar con un <@&750492134695764059> o un <@&750491866570686535> y seguro te ayudan a solucionar el problema!", inline=False)
        embed.add_field(name="Algunos comandos de utilidad", value="_Son muy utiles!_", inline=False)
        embed.add_field(name="!ayuda", value="Este comando te muestra toda la lista de comandos", inline=False)
        embed.add_field(name="!nivel", value="Una vez que envíes algunos mensajes, usa este comando para conocer tu nivel.", inline=False)
        embed.add_field(name="!rank", value="Este comando muestra los 5 usuarios con más nivel en el servidor.", inline=False)
        embed.add_field(name="!botinfo", value="Este comando te muestra información extra acerca del bot, así como también, el código fuente!", inline=False)
        embed.add_field(name="----------------", value="<a:Aprobado:784983108663246908> Recordá que nosotros nos guiamos por los [términos y condiciones de discord](https://www.discord.com/terms) y por las [directivas de la comunidad](https://www.discord.com/guidelines).", inline=False)
        welcome_message = await ctx.send(embed=embed)

    @commands.command(name="msginfo")
    @commands.has_permissions(manage_guild = True)
    async def msginfo(self,ctx):
        await ctx.channel.send(f"Contexto: \"{ctx}\"\n\nContexto.message: \"{ctx.message}\"\n\nContenido\"{ctx.message.content}\"\n\n\"reply? {ctx.message.reference}\"")


    @commands.command(name="reaccion",aliases=["Reaccion","react","React","Reacciones","reacciones"])
    async def msginfo(self,ctx,*, mensaje:str=None):
        if mensaje == None:
            await (await ctx.send("Enviá un mensaje!")).delete(delay=10)
            return
        if ctx.message.reference == None:
            await (await ctx.send("Respondé al mensaje que querés que reaccione!")).delete(delay=10)
            return

        mensaje = mensaje.lower()
        mensaje = mensaje.replace(" ","")
        if len(mensaje) > 15:
            await (await ctx.send("El mensaje no puede tener más de 15 carácteres!")).delete(delay=10)
            return
        mensaje = unidecode(mensaje)

        await (ctx.message).delete(delay=3)

        letras_dict = {
        'a': "🇦",
        'b': "🇧",
        'c': "🇨",
        'd': "🇩",
        'e': "🇪",
        'f': "🇫",
        'g': "🇬",
        'h': "🇭",
        'i': "🇮",
        'j': "🇯",
        'k': "🇰",
        'l': "🇱",
        'm': "🇲",
        'n': "🇳",
        'o': "🇴",
        'p': "🇵",
        'q': "🇶",
        'r': "🇷",
        's': "🇸",
        't': "🇹",
        'u': "🇺",
        'v': "🇻",
        'w': "🇼",
        'x': "🇽",
        'y': "🇾",
        'z': "🇿",
        '0': "0️⃣",
        '1': "1️⃣",
        '2': "2️⃣",
        '3': "3️⃣",
        '4': "4️⃣",
        '5': "5️⃣",
        '6': "6️⃣",
        '7': "7️⃣",
        '8': "8️⃣",
        '9': "9️⃣",
        }

        repetidas = set(i for i in mensaje if mensaje.count(i)>1)
        lista = []
        for i in repetidas:
            lista.append(i)
        if len(repetidas) >= 1:
            await (await ctx.send(f"El mensaje no puede contener letras repetidas!\nLetras repetidas:{lista}")).delete(delay=10)
            return

        msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)

        for letra in mensaje:
            if letra == "ñ":
                continue
            await msg.add_reaction(letras_dict[letra])



    

def setup(bot):
    bot.add_cog(Misc(bot))
