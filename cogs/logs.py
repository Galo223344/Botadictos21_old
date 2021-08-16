import discord
import json
import asyncio
from datetime import datetime
from discord.ext import commands
from __main__ import admin_ids


# TODO: Comentar codigo. Mejorar logs (Hacer más bonitos)


class Logs(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    with open('config.json', 'r') as f:
        configjson = json.load(f)
        global logchannel
        logchannel = configjson["logchannel"]
        global gvchannel
        gvchannel = configjson["gvchannel"]
        global sugchannel
        sugchannel = configjson["sugchannel"]

    with open('ignorelist.txt', 'r') as file:
        global ignorelist
        ignorelist = []
        for line in file:
            ignoree = line[:-1]
            ignorelist.append(int(ignoree))

    @commands.Cog.listener()
    async def on_ready(self):
        print ("Log cog is ready")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author == self.bot.user:
            return

        if message.channel.id in ignorelist:
            return

        embed=discord.Embed(title=f"{message.author} eliminó un mensaje en {message.channel}", description="", timestamp= datetime.now(), color=0xff0000)
        embed.add_field(name= "Mensaje eliminado:" ,value=f"\"{message.content}\"", inline=True)
        embed.set_thumbnail(url=message.author.avatar_url)
        embed.set_footer(text=f"ID del usuario: {message.author.id}") 
        channel=self.bot.get_channel(logchannel)

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author == self.bot.user:
            return

        if before.channel.id in ignorelist:
            return

        link = 'https://discord.com/channels/guild_id/channel_id/message_id'.split('/')
        server = before.guild.id
        channel = before.channel.id
        message = after.id

        link[4] =  int(server)
        link[5] = int(channel)
        link[6] = int(message)

        embed=discord.Embed(title=f"{before.author} editó un mensaje, has click para ir al mensaje", url = f"{link[0]}/{link[1]}/{link[2]}/{link[3]}/{link[4]}/{link[5]}/{link[6]}", description="", timestamp= datetime.now(), color=0x00b7ff)
        embed.add_field(name= "Mensaje original:" ,value=before.content, inline=True)
        embed.add_field(name= "Nuevo mensaje" ,value=after.content, inline=True)
        embed.set_thumbnail(url=before.author.avatar_url)
        embed.set_footer(text=f"ID del usuario: {before.author.id}") 

        channel=self.bot.get_channel(logchannel)

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        for channel in member.guild.channels:
            if str(channel) == "👋bienvenidos":
                await channel.send(f"¡Bienvenido al servidor, {member.mention}!")

        channel=self.bot.get_channel(logchannel)
        embed=discord.Embed(title=f"El usuario {member} se ha unido al servidor", timestamp= datetime.now(), color=0x400040)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"ID del usuario: {member.id}") 

        await channel.send(embed=embed)

        await asyncio.sleep(172800)

        Role = discord.utils.get(member.guild.roles, name="La People👤")
        if Role in member.roles:
            return
        else:
            embed=discord.Embed(title="¡Hola! Detecté que no aceptaste las reglas y quiero saber porqué:", description="¿Hay algo que no está funcionando como debería, o es que solamente te olvidaste? :)", color=0x008080)
            embed.set_footer(text=f"Este es un mensaje automatico, si crees que se envió por error, reportalo.", icon_url=self.bot.user.avatar_url)
            await member.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        for channel in member.guild.channels:
            if str(channel) == "👋bienvenidos":
                await channel.send(f"{member} nos abandonó :( <a:Adios:784983908747968513>")

        channel=self.bot.get_channel(logchannel)
        embed=discord.Embed(title=f"El usuario {member} ha abandonado el servidor", timestamp= datetime.now(), color=0xff0000)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"ID del usuario: {member.id}") 

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user: discord.User):
        info = await guild.fetch_ban(user)

        channel=self.bot.get_channel(logchannel)
        embed=discord.Embed(title=f"El usuario {user} ha sido baneado del servidor", timestamp= datetime.now(), color=0xff0000)
        embed.add_field(name= "Razón:" ,value=info[0], inline=True)
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_footer(text=f"ID del usuario: {user.id}") 

        await channel.send(embed=embed)



    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        channell=self.bot.get_channel(logchannel)
        embed=discord.Embed(title=f"El canal \"{channel.name}\" ha sido eliminado", timestamp= datetime.now(), color=0xff0000)

        await channell.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        channell=self.bot.get_channel(logchannel)
        embed=discord.Embed(title=f"El canal \"{channel.name}\" ha sido creado", timestamp= datetime.now(), color=0x2bff00)

        await channell.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        cambiadonombre = True
        cambiadoposicion = True
        cambioderoles = True

        if before.name == after.name:
            cambiadonombre = False

        if before.position == after.position:
            cambiadoposicion = False

        if before.changed_roles != after.changed_roles:
            return


        channell=self.bot.get_channel(logchannel)
        embed=discord.Embed(title=f" Se ha editado {before} ", timestamp= datetime.now(), color=0xff6600)

        if cambiadonombre:
            embed.add_field(name= "Nombre anterior:" ,value=before.name, inline=True)
            embed.add_field(name= "Nombre nuevo:" ,value=after.name, inline=True)

        if cambiadoposicion:
            embed.add_field(name= "Posición anterior:" ,value=before.position+1, inline=True)
            embed.add_field(name= "Posición nueva:" ,value=after.position+1, inline=True)

        if not cambiadoposicion and not cambiadonombre:
            return
        await channell.send(embed=embed)


    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        channel = self.bot.get_channel(logchannel)
        embed=discord.Embed(title="Se ha creado un nuevo rol:", timestamp= datetime.now(), color=0x2bff00)
        embed.add_field(name= "Nombre:" ,value=role.name, inline=True)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        channel = self.bot.get_channel(logchannel)
        embed=discord.Embed(title="Se ha eliminado un rol:", timestamp= datetime.now(), color=0xff0000)
        embed.add_field(name= "Nombre:" ,value=role.name, inline=True)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):


        channel = self.bot.get_channel(logchannel)
        embed=discord.Embed(title="Se ha editado un rol:", timestamp= datetime.now(), color=0xff6600)
        embed.add_field(name= "Rol editado:" ,value=after.mention, inline=False)

        permisosa=[]
        permisosb=[]
        nuevospermisos = False
        msg=""

        if before.name != after.name:
            embed.add_field(name= "Nombre anterior:" ,value=before.name, inline=True)
            embed.add_field(name= "Nombre nuevo:" ,value=after.name, inline=True)
        if before.permissions != after.permissions:

            for i in iter(after.permissions):
                if i[1] == True:
                    permisosa.append(i[0])

            for i in iter(before.permissions):
                if i[1] == True:
                    permisosb.append(i[0])

            if all(item in permisosa for item in permisosb):
                # print("nuevos permisos")
                nuevospermisos = True

                permisosf = permisosa

                for i in permisosa:
                    for k in permisosb:
                        for j in permisosf:
                            if (i and k == j):
                                permisosf.remove(j)
            else:
                # print("No hay nuevos permisos")

                permisosf = permisosb

                for i in permisosb:
                    for k in permisosa:
                        for j in permisosf:
                            if (i and k == j):
                                permisosf.remove(j)

            for i in permisosf:
                msg = msg + i + '\n'


            if nuevospermisos:
                embed.add_field(name= "Permisos nuevos:" ,value=msg, inline=True)

            else:
                embed.add_field(name= "Permisos quitados:" ,value=msg, inline=True)


            # embed.add_field(name= "Permisos anteriores:" ,value=before.permissions, inline=True)
            # embed.add_field(name= "Permisos nuevos:" ,value=after.permissions, inline=True)





        if before.name == after.name and before.permissions == after.permissions:
            return

        await channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_member_update(self, before, after):

        # print("Member updated")

        cambioderoles = False
        cambiodenick = False
        nuevosroles = False

        if before.roles == after.roles and before.nick == after.nick:
            return

        if before.roles != after.roles:
            cambioderoles = True
            if all(item in after.roles for item in before.roles):
                # print("roles agregados")
                # print(after.roles)
                nuevosroles = True

                lista1 = after.roles

                for i in after.roles:
                    for k in before.roles:
                        for j in lista1:
                            if (i and k == j):
                                lista1.remove(j)
            else:
                # print("roles quitados")

                lista1 = before.roles
                for i in before.roles:
                    for k in after.roles:
                        for j in lista1:
                            if (i and k == j):
                                lista1.remove(j)
            # print(lista1)


        if before.nick != after.nick:
            # print("encontrado cambio de nick")
            cambiodenick = True


        channel = self.bot.get_channel(logchannel)

        if cambiodenick:
            embed=discord.Embed(title=f"Se ha cambiado el apodo de {before.name}#{before.discriminator}", timestamp= datetime.now(), color=0xff6600)
            embed.add_field(name= "Apodo anterior:" ,value=before.nick, inline=False)
            embed.add_field(name= "Apodo nuevo:" ,value=after.nick, inline=False)
            embed.set_footer(text=f"ID del usuario: {before.id}")
            embed.set_thumbnail(url=before.avatar_url)
        elif cambioderoles:

            if nuevosroles == True:

                if lista1[0].name.lower() == ("silenciado" or "la people👤"):
                    return

                embed=discord.Embed(title=f"Se ha agregado un rol a {before.name}#{before.discriminator}", timestamp= datetime.now(), color=0x2bff00)
                embed.add_field(name= "Rol agregado:" ,value=f"{lista1[0].mention}", inline=False)
                embed.set_footer(text=f"ID del usuario: {before.id}")
                embed.set_thumbnail(url=before.avatar_url)


            elif nuevosroles == False:

                if lista1[0].name.lower() == ("silenciado" or "La People👤"):
                    return

                embed=discord.Embed(title=f"Se ha quitado un rol a {before.name}#{before.discriminator}", timestamp= datetime.now(), color=0xff0000)
                embed.add_field(name= "Rol quitado:" ,value=f"{lista1[0].mention}", inline=False)
                embed.set_footer(text=f"ID del usuario: {before.id}")
                embed.set_thumbnail(url=before.avatar_url)
            else:
                return

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):

        embed=discord.Embed(title="Se ha eliminado un rol", timestamp= datetime.now(), color=0xff0000)
        embed.add_field(name= "Rol elminado:" ,value=role.name, inline=False)
        
        channel = self.bot.get_channel(logchannel)
        await channel.send(embed=embed)



    @commands.Cog.listener()
    async def on_guild_role_create(self, role):

        embed=discord.Embed(title="Se ha creado un rol", timestamp= datetime.now(), color=0x2bff00)
        embed.add_field(name= "Rol creado:" ,value=role.mention, inline=False)

        channel = self.bot.get_channel(logchannel)
        await channel.send(embed=embed)



    @commands.Cog.listener()
    async def on_guild_update(self, before, after):

        cambiodenombre = False
        cambioderegion = False
        cambiodeicon = False
        cambiodedescripcion = False

        if before.name != after.name:
            cambiodenombre = True

        if before.region != after.region:
            cambioderegion = True

        if before.icon != after.icon:
            cambiodeicon = True

        # if before.description != after.description:
        #     cambiodedescripcion = True

        if not cambiodenombre and not cambioderegion and not cambiodeicon:
            return

        embed=discord.Embed(title="Se ha editado el servidor", timestamp= datetime.now(), color=0xff6600)

        if cambiodenombre:
            embed.add_field(name= "Se ha cambiado el nombre del servidor" ,value=f"**Nombre anterior:** \"{before.name}\",\n **Nombre nuevo:** \"{after.name}\"", inline=False)

        if cambioderegion:
            embed.add_field(name= "Se ha cambiado la región del servidor" ,value=f"**Región anterior:** {str(before.region).capitalize()},\n **Región nueva:** {str(after.region).capitalize()}", inline=False)

        if cambiodeicon:
            embed.add_field(name= "Se ha cambiado el icono del servidor" ,value=f"**Icono anterior:** {before.icon_url},\n **Icono nuevo:** {after.icon_url}", inline=False)

        # if cambiodedescripcion:
        #     embed.add_field(name= "Se ha cambiado la descripción del servidor" ,value=f"Descripción anterior: **{before.description}**, Descripción nueva: **{after.description}**", inline=False)

        channel = self.bot.get_channel(logchannel)
        await channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        entradacanal = False
        desconcanal = False
        cammbiocanal = False

        forcemute = False
        forceunmute = False

        forcedeaf = False
        forceundeaf = False

        selfmute = False
        selfunmute = False

        selfdeaf = False
        selfundeaf = False

        if after.channel is not None and before.channel is None:
            entradacanal = True
        if after.channel is None and before.channel is not None:
            desconcanal = True
        if before.channel != after.channel and after.channel is not None and before.channel is not None:
            cammbiocanal = True

        if after.mute == True and before.mute == False:
            forcemute = True
        if after.mute == False and before.mute == True:
            forceunmute = True

        if after.deaf == True and before.deaf == False:
            forcedeaf = True
        if after.deaf == False and before.deaf == True:
            forceundeaf = True


        if after.self_mute == True and before.self_mute == False:
            selfmute = True
        if after.self_mute == False and before.self_mute == True:
            selfunmute = True

        if after.self_deaf == True and before.self_deaf == False:
            selfdeaf = True
        if after.self_deaf == False and before.self_deaf == True:
            selfundeaf = True


        if entradacanal:
            embed=discord.Embed(title=f"El usuario {member} entró a un canal de voz", timestamp= datetime.now(), color=0x00b7ff)
            embed.add_field(name= "------" ,value=f"{member.mention} entró a {after.channel.mention}", inline=False)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(text=f"ID del usuario: {member.id}")

            channel = self.bot.get_channel(logchannel)
            await channel.send(embed=embed)

        if desconcanal:
            embed=discord.Embed(title=f"El usuario {member} salió de un canal de voz", timestamp= datetime.now(), color=0x00b7ff)
            embed.add_field(name= "------" ,value=f"{member.mention} salió de {before.channel.mention}", inline=False)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(text=f"ID del usuario: {member.id}")

            channel = self.bot.get_channel(logchannel)
            await channel.send(embed=embed)

        if cammbiocanal:
            embed=discord.Embed(title=f"El usuario {member} se cambió de canal de voz", timestamp= datetime.now(), color=0x00b7ff)
            embed.add_field(name= "------" ,value=f"{member.mention} cambió del canal {before.channel.mention} a {after.channel.mention}", inline=False)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(text=f"ID del usuario: {member.id}")

            channel = self.bot.get_channel(logchannel)
            await channel.send(embed=embed)

        if forcemute:
            embed=discord.Embed(title=f"El usuario {member} fue silenciado", timestamp= datetime.now(), color=0x00b7ff)
            embed.add_field(name= "------" ,value=f"{member.mention} fue silenciado por un moderador", inline=False)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(text=f"ID del usuario: {member.id}")

            channel = self.bot.get_channel(logchannel)
            await channel.send(embed=embed)

        if forceunmute:
            embed=discord.Embed(title=f"El usuario {member} fue des-silenciado", timestamp= datetime.now(), color=0x00b7ff)
            embed.add_field(name= "------" ,value=f"{member.mention} fue des-silenciado por un moderador", inline=False)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(text=f"ID del usuario: {member.id}")

            channel = self.bot.get_channel(logchannel)
            await channel.send(embed=embed)

        if selfmute:
            embed=discord.Embed(title=f"El usuario {member} se silenció", timestamp= datetime.now(), color=0x00b7ff)
            embed.add_field(name= "------" ,value=f"{member.mention} se silenció", inline=False)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(text=f"ID del usuario: {member.id}")

            channel = self.bot.get_channel(logchannel)
            await channel.send(embed=embed)

        if selfunmute:
            embed=discord.Embed(title=f"El usuario {member} se des-silenció", timestamp= datetime.now(), color=0x00b7ff)
            embed.add_field(name= "------" ,value=f"{member.mention} se des-silenció", inline=False)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(text=f"ID del usuario: {member.id}")

            channel = self.bot.get_channel(logchannel)
            await channel.send(embed=embed)

        if forcedeaf:
            embed=discord.Embed(title=f"El usuario {member} fue ensordecido", timestamp= datetime.now(), color=0x00b7ff)
            embed.add_field(name= "------" ,value=f"{member.mention} fue ensordecido por un moderador", inline=False)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(text=f"ID del usuario: {member.id}")

            channel = self.bot.get_channel(logchannel)
            await channel.send(embed=embed)

        if forceundeaf:
            embed=discord.Embed(title=f"El usuario {member} fue des-ensordecido", timestamp= datetime.now(), color=0x00b7ff)
            embed.add_field(name= "------" ,value=f"{member.mention} fue des-ensordecido por un moderador", inline=False)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(text=f"ID del usuario: {member.id}")

            channel = self.bot.get_channel(logchannel)
            await channel.send(embed=embed)

        if selfdeaf:
            embed=discord.Embed(title=f"El usuario {member} se ensordeció", timestamp= datetime.now(), color=0x00b7ff)
            embed.add_field(name= "------" ,value=f"{member.mention} se ensordeció", inline=False)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(text=f"ID del usuario: {member.id}")

            channel = self.bot.get_channel(logchannel)
            await channel.send(embed=embed)

        if selfundeaf:
            embed=discord.Embed(title=f"El usuario {member} se des-ensordeció", timestamp= datetime.now(), color=0x00b7ff)
            embed.add_field(name= "------" ,value=f"{member.mention} se des-ensordeció", inline=False)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(text=f"ID del usuario: {member.id}")

            channel = self.bot.get_channel(logchannel)
            await channel.send(embed=embed)




    # logchannel

    @commands.command(name='logchannel', aliases=["logchan","Logchan","Logchannel"])
    async def logchan(self, ctx):
        if ctx.author.id not in admin_ids:
            embed=discord.Embed(title="¡No tienes permisos para utilizar este comando!", description="Necesitas contar con el permiso `BOT_OPERATOR`", color=0xff0000)
            embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        global logchannel

        logchannel = ctx.channel.id

        with open('config.json', 'r') as f:
            logchan = json.load(f)

        logchan["logchannel"] = logchannel

        await ctx.send(f"Logchannel cambiado a #{ctx.channel}")

        with open("config.json", "w") as outfile:
            json.dump(logchan, outfile)

    # GVchannel

    @commands.command(name='gvchannel', aliases=["Gvchannel","gvchan","Gvchan"])
    async def gvchan(self, ctx):
        if ctx.author.id not in admin_ids:
            embed=discord.Embed(title="¡No tienes permisos para utilizar este comando!", description="Necesitas contar con el permiso `BOT_OPERATOR`", color=0xff0000)
            embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return

        global gvchannel
        gvchannel = ctx.channel.id

        with open('config.json', 'r') as f:
            config = json.load(f)

        config["gvchannel"] = gvchannel

        await ctx.send(f"GVchannel ha sido cambiado al canal #{ctx.channel}")

        with open("config.json", "w") as outfile:
            json.dump(config, outfile)


    # Ignore

    @commands.command(name="ignore")
    async def ignor(self, ctx):
        if ctx.author.id not in admin_ids:
            embed=discord.Embed(title="¡No tienes permisos para utilizar este comando!", description="Necesitas contar con el permiso `BOT_OPERATOR`", color=0xff0000)
            embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        global ignorelist

        if ctx.channel.id in ignorelist:
            ignorelist.remove(ctx.channel.id)
            await ctx.send(f"El canal #{ctx.channel} ha sido eliminado de la ignorelist")

            with open("ignorelist.txt",'w') as ofile:
                for i in ignorelist:
                    ofile.write(f"{i} \n")
            return


        ignorelist.append(ctx.channel.id)

        await ctx.send(f"El canal #{ctx.channel} ha sido agregado a la ignorelist")

        with open("ignorelist.txt",'w') as ofile:
            for i in ignorelist:
                ofile.write(f"{i} \n")

    # ignorelist

    @commands.command(name="ignorelist")
    async def ignorlist(self,ctx):
        if ctx.author.id not in admin_ids:
            embed=discord.Embed(title="¡No tienes permisos para utilizar este comando!", description="Necesitas contar con el permiso `BOT_OPERATOR`", color=0xff0000)
            embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
            
        channelnames = []
        global ignorelist
        for i in ignorelist:
            try:
                nameee = self.bot.get_channel(i)
                channelnames.append(nameee.name)
            except:
                pass
        await ctx.send("```Canales ignorados por el bot:\n"+''.join(f"        • {i}\n" for i in channelnames)+"```")
    
    #sugchannel

    @commands.command(name='sugchannel', aliases=["Sugchannel","sugchan","Sugchan"])
    async def sugchan(self, ctx):
        if ctx.author.id not in admin_ids:
            embed=discord.Embed(title="¡No tienes permisos para utilizar este comando!", description="Necesitas contar con el permiso `BOT_OPERATOR`", color=0xff0000)
            embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return

        global sugchannel
        sugchannel = ctx.channel.id

        with open('config.json', 'r') as f:
            config = json.load(f)

        config["sugchannel"] = sugchannel

        await ctx.send(f"Sugchannel ha sido cambiado al canal #{ctx.channel}")

        with open("config.json", "w") as outfile:
            json.dump(config, outfile)

def predicate(event):
    return event.action is discord.AuditLogAction.ban

def setup(bot):
    bot.add_cog(Logs(bot))
