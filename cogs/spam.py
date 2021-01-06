import discord
import asyncio
from datetime import datetime
from discord.ext import commands
from cogs.logs import logchannel


# TODO: En teoría nada ;)


class Spam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print ("spam cog is ready")

    @commands.Cog.listener()
    async def on_message(self, message):
        # Si el mensaje fue enviado por mensaje privado nos chupa un huevo
        if message.channel.type is discord.ChannelType.private:
            return
        # Revisamos si el que envió el mensaje es un bot
        if message.author.bot == True:
            return
        # Revisamos si el que envió el mensaje es un mod/admin
        if message.author.guild_permissions.kick_members:
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
                mensaje_procesado.append(item)


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
                else:
                    # Si no lo está, significa que es una invitación de otro servidor. Así que avisamos al usuario y eliminamos el mensaje
                    warn = await message.channel.send(f"{message.author.mention}, por favor evita enviar invitaciones de otros servers de discord :)")
                    await message.delete()
                    channel = self.bot.get_channel(logchannel)
                    embed=discord.Embed(title=f"{message.author.mention} Trató de enviar una invitación a otro servidor", timestamp= datetime.now(), color=0x804000)
                    embed.add_field(name="Mensaje original:", value=message.content, inline=False)
                    embed.set_thumbnail(url=message.author.avatar_url)
                    await channel.send(embed=embed)
                    await asyncio.sleep(15)
                    await warn.delete()
                    return

            # Comenzamos el checkeo de discord.com
            if "discord.com" in mensaje_procesado:
                # Si el siguiente item despues de "invite" en la lista de mensaje_procesado está en la lista de codigos
                if mensaje_procesado[mensaje_procesado.index("invite")+1] in codigos:
                    # print("No es spam (invite)")
                    return
                else:
                    # Si no lo está, significa que es una invitación de otro servidor. Así que avisamos al usuario y eliminamos el mensaje
                    warn = await message.channel.send(f"{message.author}, por favor evita enviar invitaciones de otros servers de discord :)")
                    await message.delete()
                    channel = self.bot.get_channel(logchannel)
                    embed=discord.Embed(title=f"{message.author.mention} Trató de enviar una invitación a otro servidor", timestamp= datetime.now(), color=0x400080)
                    embed.add_field(name="Mensaje original:", value=message.content, inline=False)
                    embed.set_footer(text=datetime.now())
                    embed.set_thumbnail(url=message.author.avatar_url)
                    await channel.send(embed=embed)
                    await asyncio.sleep(15)
                    await warn.delete()
                    return





def setup(bot):
    bot.add_cog(Spam(bot))
