import discord
import json
import re
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from cogs.logs import logchannel
import asyncio


# TODO: Comentar el codigo


class Temp(commands.Cog):
    def __init__(self,bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print ("Temp cog is ready")
        # self.bot.loop.create_task(tiempocheck(self))
        # print("antes de iniciar el task")
        self.tiempocheck.start()
        # print("despues de iniciar el task")


    @commands.has_permissions(ban_members=True)
    @commands.command(name="tempban",aliases=["Tempban"])
    async def tempban(self, ctx, member:discord.User=None, tiempo=None, *, reason=None):
        if member == None or member == ctx.message.author:
            embed=discord.Embed(title="¡Usuario no valido!", description="", color=0xff0000)
            embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed=embed)
            return


        banlist = []

        if tiempo == None:
            embed=discord.Embed(title="Por favor, especifica un tiempo de la siguiente manera:", description="`1m 1h 1d`", color=0xff0000)
            embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        if reason == None:
            reason = "La razón no ha sido especificada."

        

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
            embed=discord.Embed(title="¡Tiempo invalido!", description="", color=0xff0000)
            embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed=embed)
            return

        # print(f"dias = {dias}")
        # print(f"horas = {horas}")
        # print(f"minutos = {minutos}")


        tiempodevuelta = datetime.now().replace(microsecond=0,second=0) + timedelta(minutes=minutos,hours=horas,days=dias)

        banlist.append(f"{member.id};{tiempodevuelta};{ctx.guild.id}")
        # print("agregado el primer valor a banlist")
        tiempo_formateado = tiempodevuelta.strftime("%d/%m/%Y %H:%M")
        embed=discord.Embed(title=f"Has sido baneado temporalmente de {ctx.guild.name} por la siguiente razón:", description=f"{reason}", color=0x008080)
        embed.add_field(name="Puedes apelar al baneo aquí:", value="Haz [click aquí](https://gtadictos21.com/apelacion-ban) para rellenar el formulario de apelaciones.", inline=True)
        embed.set_footer(text=f" Baneo efectuado por {ctx.message.author.name}. Expira el dia: {tiempo_formateado}.", icon_url=ctx.author.avatar_url)
        await member.send(embed=embed)

        with open('tempban.txt', 'r') as file:
            for line in file:
                bann = line[:-1].strip()
                # print(f"valor de bann: {bann}")
                banlist.append(bann)
                # print(f"valor de banlist: {banlist}")
            # print("terminado primer for loop")

        with open("tempban.txt",'w') as ofile:
            for i in banlist:
                ofile.write(f"{i.strip()} \n")
            # print("terminado segundo for loop")
        embed=discord.Embed(title=f"El usuario {member.name} ha sido baneado, y será desbaneado el dia: ", description=f"{tiempo_formateado}", color=0x008080)
        embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        await ctx.guild.ban(member, reason=reason)


        # print(f"Valor final de banlist: {banlist}")



    @commands.command(name="unasimpleprueba")
    async def unasimpleprueba(self, ctx):
    	await ctx.channel.send("Buenaaaass!  -el gaspi")
    	print("print de prueba")


    @commands.has_permissions(manage_roles=True)
    @commands.command(name="tempmute",aliases=["Tempmute"])
    async def tempmute(self, ctx, member:discord.Member=None, * , tiempo=None,):
        if member == None or member == ctx.message.author:
            embed=discord.Embed(title="¡Usuario no valido!", description="", color=0xff0000)
            embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed=embed)
            return

        Role = discord.utils.get(member.guild.roles, name="Silenciado")
        role2 = discord.utils.get(member.guild.roles, name="La People👤")
        
        if Role in member.roles:
            embed=discord.Embed(title="¡El usuario ya se encuentra silenciado!", description="", color=0xff0000)
            embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return


        mutelist = []

        if tiempo == None:
            embed=discord.Embed(title="Por favor, especifica un tiempo de la siguiente manera:", description="`1m 1h 1d`", color=0xff0000)
            embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
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

        # print(f"dias = {dias}")
        # print(f"horas = {horas}")
        # print(f"minutos = {minutos}")

        if minutos == 0 and horas == 0 and dias == 0:
            embed=discord.Embed(title="¡Tiempo invalido!", description="", color=0xff0000)
            embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return


        tiempodevuelta = datetime.now().replace(microsecond=0,second=0) + timedelta(minutes=minutos,hours=horas,days=dias)

        mutelist.append(f"{member.id};{tiempodevuelta};{ctx.guild.id}")
        # print("agregado el primer valor a banlist")

        tiempo_formateado = tiempodevuelta.strftime("%d/%m/%Y %H:%M")

        with open('tempmute.txt', 'r') as file:
            for line in file:
                muteee = line[:-1].strip()
                mutelist.append(muteee)

        with open("tempmute.txt",'w') as ofile:
            for i in mutelist:
                ofile.write(f"{i.strip()} \n")
            # print("terminado segundo for loop")

        await member.add_roles(Role)
        await member.remove_roles(role2)

        embed=discord.Embed(title=f"El usuario {member.name} ha sido muteado, y será desmuteado el dia: ", description=f"{tiempo_formateado}", color=0x008080)
        embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @tasks.loop(minutes=1)
    async def tiempocheck(self):
        # print("principio de task")
        unbanlist = []

        with open('tempban.txt', 'r') as file:
            for line in file:
                bannn = line[:-1].strip()
                # print(f"valor de bann: {bann}")
                unbanlist.append(bannn)

        with open('tempban.txt', 'r') as file:
            for line in file:
                currentuser = line[:-1].strip()
                userlist = currentuser.split(";")
                unbandate =  datetime.strptime(userlist[1],'%Y-%m-%d %H:%M:%S')
                if unbandate < datetime.now():
                    unbanlist.pop(unbanlist.index(f"{userlist[0]};{userlist[1]};{userlist[2]}"))
                    usuario = await self.bot.fetch_user(int(userlist[0]))
                    guild = await self.bot.fetch_guild(int(userlist[2]))
                    channel=self.bot.get_channel(logchannel)
                    try:
                        await guild.unban(usuario, reason="Expiró el ban temporal")
                        embed=discord.Embed(title="Un usuario ha sido desbaneado:", color=0x2bff00)
                        embed.add_field(name= "Usuario desbaneado:" ,value=usuario.name, inline=True)
                        await channel.send(embed=embed)
                    except:
                        embed=discord.Embed(title="Un tempban ha fallado:", description="", color=0xff0000)
                        embed.add_field(name=f"El tempban del usuario: {usuario} ha fallado.", value="Esto puede deberse a que el usuario fue desbaneado antes de que expirara el baneo temporal o por alguna otra razón. Si el usuario sigue baneado deberian desbanearlo.", inline=True)
                        await channel.send(embed=embed)
                        # await channel.send(f"El tempban de **{usuario}** ha fallado. Esto puede deberse a que el usuario fue desbaneado antes de que expirara el baneo temporal o por alguna otra razón. Si el usuario sigue baneado deberian desbanearlo. <@388924384016072706>") "<@&750491866570686535>"

        with open("tempban.txt",'w') as ofile:
            for i in unbanlist:
                ofile.write(f"{i.strip()} \n")





        unmutelist = []

        with open('tempmute.txt', 'r') as infile:
            for line in infile:
                mutee = line[:-1].strip()
                # print(f"valor de bann: {bann}")
                unmutelist.append(mutee)

        with open('tempmute.txt', 'r') as file:
            for line in file:
                currentmuser = line[:-1].strip()
                userlistm = currentmuser.split(";")
                unmutedate =  datetime.strptime(userlistm[1],'%Y-%m-%d %H:%M:%S')
                # print(f"unmutedate = {unmutedate} ahora = {datetime.now()}")
                if unmutedate < datetime.now():
                    # print("si se detectó")
                    unmutelist.pop(unmutelist.index(f"{userlistm[0]};{userlistm[1]};{userlistm[2]}"))
                    # print("det1")
                    guild = await self.bot.fetch_guild(int(userlistm[2]))
                    # print("dect2")
                    member = await guild.fetch_member(int(userlistm[0]))
                    # print("dect3")

                    Role = discord.utils.get(member.guild.roles, name="Silenciado")
                    rolepeople = discord.utils.get(member.guild.roles, name="La People👤")
                    # print("dect4")
                    channel=self.bot.get_channel(logchannel)
                    # print("dect5")
                    if Role not in member.roles:
                        embed=discord.Embed(title="Error de tempmute:", description=f"El usuario {member.name} no se encuentra silenciado.", color=0xff0000)
                        embed.set_thumbnail(url=member.avatar_url)
                        await channel.send(embed=embed)
                        continue

                    print("Agregado rol la people")
                    # print(rolepeople)
                    await member.add_roles(rolepeople)

                    print("Sacado rol silenciado")
                    # print(Role)
                    await member.remove_roles(Role)

                    # print("dect6")
                    embed=discord.Embed(title="Un usuario ha sido desbaneado:", color=0x2bff00)
                    # print("dect7")
                    embed.add_field(name="Usuario desmuteado:" ,value=member.name, inline=True)
                    embed.set_thumbnail(url=member.avatar_url)
                    # print("dect8")
                    await channel.send(embed=embed)

        with open("tempmute.txt",'w') as ofile:
            for i in unmutelist:
                ofile.write(f"{i.strip()} \n")

        # await asyncio.sleep(60)
        # print("1 minuto ha pasado")

def setup(bot):
    bot.add_cog(Temp(bot))
