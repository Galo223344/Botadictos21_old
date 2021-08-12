import discord
import asyncio
from datetime import datetime
from discord.ext import commands
from cogs.logs import logchannel
from __main__ import admin_ids




class Spam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Cargamos la lista de spam en la variable listaspam
    global listaspam
    listaspam = list()
    with open("spamlist.txt", "r") as archivo:
        for linea in archivo.readlines():
            listaspam.append(linea[:-1])
    print("Spamlist.txt ha sido cargada")
    @commands.Cog.listener()
    async def on_ready(self):
        print ("spam cog is ready")

    @commands.Cog.listener()
    async def on_message(self, message):

        # Si el mensaje fue enviado por mensaje privado nos chupa un huevo
        if message.channel.type is discord.ChannelType.private:
            return


        # La verdad no se porque hay que hacer esto, pero un día dejó de funcionar lol
        guild = message.guild
        member = guild.get_member(message.author.id)

        
        # Revisamos si el que envió el mensaje es un mod/admin
        if member.guild_permissions.kick_members:
            # print("lo es")
            return

        mensaje_procesado2 = []
        mensaje_procesado = []
        # Convertimos el mensaje a minusculas para evitar que eviten el sistema
        mensaje_minus = message.content.lower()
        # Lo separamos por "/"
        mensaje_procesado1 = mensaje_minus.split("/")
        # Lo separamos por espacios así podemos obtener el codigo de invitacion en un solo item de lista
        for i in mensaje_procesado1:
            i = i.split(" ")
            mensaje_procesado2.append(i)

        # Aplanamos la lista

        for sublist in mensaje_procesado2:
            for item in sublist:
                mensaje_procesado.append(item.replace("|",""))


        # print(mensaje_procesado)

        # Revisamos si el mensaje tiene "discord.gg" O "discord.com" seguido de un "invite"

        if "discord.gg" in mensaje_procesado or ("discord.com" in mensaje_procesado and mensaje_procesado[mensaje_procesado.index("discord.com")+1] == "invite"):
            # print("Se encontró link de invitacion de discord")

            codigos = []


            # Conseguimos las invitaciones validas actuales
            invitaciones = await message.guild.invites()

            # Separamos los codigos de las invitaciones y los guardamos en la lista "codigos"
            for i in invitaciones:
                i = i.code
                codigos.append(i)
            # print(codigos)

            # Comenzamos el checkeo de discord.gg
            if "discord.gg" in mensaje_procesado:
                # Si el siguiente item despues de "discord.gg" en la lista de mensaje_procesado está en la lista de codigos
                if mensaje_procesado[mensaje_procesado.index("discord.gg")+1] in codigos:
                    # print("No es spam")
                    return
                elif mensaje_procesado[mensaje_procesado.index("discord.gg")+1] == "gtadictos21":
                    return
                else:
                    # Si no lo está, significa que es una invitación de otro servidor. Así que avisamos al usuario y eliminamos el mensaje
                    embed=discord.Embed(title="Por favor, evitá enviar invitaciones de otros servidores de Discord :D", description="", color=0xff0000)
                    embed.set_footer(text=f"Este es un mensaje automatico, si crees que se envió por error, reportalo.", icon_url=self.bot.user.avatar_url)
                    await message.author.send(message.author.mention, embed=embed)
                    await message.delete()
                    channel = self.bot.get_channel(logchannel)
                    embed=discord.Embed(title=f" El usuario {message.author} trató de enviar una invitación a otro servidor.", timestamp= datetime.now(), color=0x804000)
                    embed.add_field(name="Mensaje original:", value=message.content, inline=False)
                    embed.set_thumbnail(url=message.author.avatar_url)
                    await channel.send(embed=embed)
                    await asyncio.sleep(15)
                    return

            # Comenzamos el checkeo de discord.com
            if "discord.com" in mensaje_procesado:
                # Si el siguiente item despues de "invite" en la lista de mensaje_procesado está en la lista de codigos
                if mensaje_procesado[mensaje_procesado.index("invite")+1] in codigos:
                    # print("No es spam (invite)")
                    return
                else:
                    # Si no lo está, significa que es una invitación de otro servidor. Así que avisamos al usuario y eliminamos el mensaje
                    embed=discord.Embed(title="Por favor, evitá enviar invitaciones de otros servidores de Discord :D", description="", color=0xff0000)
                    embed.set_footer(text=f"Este es un mensaje automatico, si crees que se envió por error, reportalo.", icon_url=self.bot.user.avatar_url)
                    await message.author.send(message.author.mention, embed=embed)
                    await message.delete()
                    await message.delete()
                    channel = self.bot.get_channel(logchannel)
                    embed=discord.Embed(title=f" El usuario {message.author} trató de enviar una invitación a otro servidor.", timestamp= datetime.now(), color=0x400080)
                    embed.add_field(name="Mensaje original:", value=message.content, inline=False)
                    embed.set_footer(text=datetime.now())
                    embed.set_thumbnail(url=message.author.avatar_url)
                    await channel.send(embed=embed)
                    await asyncio.sleep(15)
                    return

        for spam in listaspam:
            # print(spam)
            if spam in mensaje_procesado:
                # print(f"{spam} encontrado en mensaje")
                await message.delete()
                embed=discord.Embed(title="Ese tipo de links están prohibidos. Por favor, comunicate con los administradores para ser desmuteado.", description="Haz click [aquí](https://Gtadictos21.com/discord) para contactarlos.", color=0xff0000)
                embed.set_footer(text=f"Este es un mensaje automatico, si crees que se envió por error, reportalo.", icon_url=self.bot.user.avatar_url)
                await message.author.send(message.author.mention, embed=embed)


                Role = discord.utils.get(member.guild.roles, name="Silenciado")
                role2 = discord.utils.get(member.guild.roles, name="La People👤")
                await member.add_roles(Role)
                await member.remove_roles(role2)

                channel = self.bot.get_channel(logchannel)
                embed=discord.Embed(title=f" El usuario {message.author} envió un link engañoso y fue muteado automaticamente.", timestamp= datetime.now(), color=0x804000)
                embed.add_field(name="Mensaje original:", value=message.content, inline=False)
                embed.set_thumbnail(url=message.author.avatar_url)
                await channel.send(embed=embed)
                return

    # Escribe links en spamlist.txt
    @commands.command(name="add")
    async def add(self, ctx, arg = None):
        if ctx.author.id not in admin_ids:

            embed=discord.Embed(title="¡No tienes permisos para utilizar este comando!", description="Necesitas contar con el permiso `BOT_OPERATOR`", color=0xff0000)
            embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
            
        if arg == None:
            embed=discord.Embed(title="¡Argumento inválido!", description=f"", color=0x008080)
            embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return


        with open('spamlist.txt','a') as file:
            file.write(f"{arg}\n")
            print(f'¡El link "{arg}" ha sido agregado a la lista de spam!')
        
        embed=discord.Embed(title="¡Un nuevo link ha sido agregado a la lista de spam!", description=f"Link agregado: {arg} ", color=0x008080)
        embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)        

    @add.error
    async def add_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title="¡No tienes permisos para utilizar este comando!", description="Necesitas contar con el permiso `BOT_OPERATOR`", color=0xff0000)
            embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

            




def setup(bot):
    bot.add_cog(Spam(bot))
