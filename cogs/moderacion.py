import discord
import asyncio
from discord.ext import commands
from cogs.logs import logchannel


# TODO: Agregar logs para cada comando. Comentar el codigo


class Moderacion(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print ("Moderacion cog is ready")



    # Ban

    @commands.command(name='ban', help='Banea a un miembro. Solo admins', aliases=["Ban"])
    @commands.has_permissions(ban_members=True)
    async def ban (self, ctx, member:discord.Member=None, *,reason =None):
        if member == None or member == ctx.message.author:
            await ctx.channel.send("Usuario no valido.")
            return
        if reason == None:
            reason = "Sin razón especificada."

        reason = reason + f" Baneo efectuado por {ctx.message.author}"

        message = f"Has sido baneado de {ctx.guild.name} por la siguente razón: \"{reason}\""
        
        try:
        	await member.send(message)
        except:
        	pass

        await ctx.guild.ban(member, reason=reason)
        await ctx.channel.send(f"{member} ha sido baneado!")


        # channel=self.bot.get_channel(logchannel)
        # embed=discord.Embed(title=f"{ctx.author} ha baneado a {member} por la siguiente razón: {reason}", color=0x400040)
        # await channel.send(embed=embed)

    @ban.error
    async def handler_ban(self, ctx,error):
    	if isinstance(error, discord.ext.commands.errors.UserNotFound):
    		await ctx.send("Usuario no encontrado")


    # Kick

    @commands.command(name='kick', help='kickea a un miembro. Solo admins', aliases=["Kick","expulsar","Expulsar"])
    @commands.has_permissions(kick_members=True)
    async def kick (self, ctx, member:discord.Member=None, *,reason=None):
        if member == None or member == ctx.message.author:
            await ctx.channel.send("Usuario no valido.")
            return
        if reason == None:
            reason = "Sin razón especificada."
        reason = reason + f" Kick efectuado por {ctx.message.author}"
        message = f"Has sido expulsado de {ctx.guild.name} por la siguente razón: {reason}"
        try:
        	await member.send(message)
        except:
        	pass
        await ctx.guild.kick(member, reason=reason)
        await ctx.channel.send(f"{member} ha sido expulsado!")


        channel=self.bot.get_channel(logchannel)
        embed=discord.Embed(title=f"{ctx.author} ha expulsado a {member} por la siguiente razón: {reason}", color=0xff0000)
        await channel.send(embed=embed)

    @kick.error
    async def handler_ban(self, ctx,error):
    	if isinstance(error, discord.ext.commands.errors.UserNotFound):
    		await ctx.send("Usuario no encontrado")

    # Silenciar

    @commands.command(name='silenciar',help='Silencia al usuario especificado', aliases=["Silenciar","mute","Mute"])
    @commands.has_permissions(manage_roles=True)
    async def silenciar(self, ctx, member:discord.Member=None, *,reason=None):
        Role = discord.utils.get(member.guild.roles, name="Silenciado")
        role2 = discord.utils.get(member.guild.roles, name="La People👤")

        if member == None or member == ctx.message.author:
            await ctx.channel.send("Usuario no valido")
            return
        if reason == None:
            reason = "Sin razon especificada"
        if Role in member.roles:
            await ctx.send("El usuario ya está silenciado")
            return

        Role = discord.utils.get(member.guild.roles, name="Silenciado")
        await member.add_roles(Role)
        await ctx.send("El usuario ha sido muteado")
        await member.remove_roles(role2)

        channel = self.bot.get_channel(logchannel)
        embed=discord.Embed(title="Usuario silenciado", color=0xff0000)
        embed.add_field(name= "Usuario silenciado:" ,value=member.mention, inline=False)
        embed.add_field(name= "Silenciado por:" ,value=ctx.message.author.mention, inline=False)
        await channel.send(embed=embed)

    @silenciar.error
    async def handler_ban(self, ctx,error):
        if isinstance(error, discord.ext.commands.errors.UserNotFound):
            await ctx.send("Usuario no encontrado")

    # Des-Silenciar/Unmute

    @commands.command(name='reactivar',help='Le saca el silencio al usuario especificado', aliases=["dessilenciar","unmute","Reactivar","Unmute","Dessilenciar","DesSilenciar"])
    @commands.has_permissions(manage_roles=True)
    async def reactivar(self, ctx, member:discord.Member=None):
        Role = discord.utils.get(member.guild.roles, name="Silenciado")

        if member == None or member == ctx.message.author:
            await ctx.channel.send("Usuario no valido")
            return
        if Role not in member.roles:
            await ctx.send("El usuario no está silenciado")
            return

        Role = discord.utils.get(member.guild.roles, name="Silenciado")
        role2 = discord.utils.get(member.guild.roles, name="La People👤")

        await member.remove_roles(Role)
        await ctx.send("El usuario ha sido desmuteado")
        await member.add_roles(role2)

        channel = self.bot.get_channel(logchannel)
        embed=discord.Embed(title="Usuario desmuteado", color=0x2bff00)
        embed.add_field(name= "Usuario desmuteado:" ,value=member.mention, inline=False)
        embed.add_field(name= "Desmuteado por:" ,value=ctx.message.author.mention, inline=False)
        await channel.send(embed=embed)

    @reactivar.error
    async def handler_ban(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.UserNotFound):
            await ctx.send("Usuario no encontrado")

    # Purgar

    @commands.command(name='purgar',help='Purga x cantidad de mensajes', aliases=["Purgar","purge","Purge","prune","Prune","eliminar","Eliminar"])
    @commands.has_permissions(manage_guild=True)
    async def purge(self, ctx,cantidad : int):
        if cantidad <= 0:
            await ctx.send("._.")
            return
        if cantidad > 500:
            await ctx.send("Se ha exedido el limite, el limite es de 500 mensajes")
            return
        await ctx.channel.purge(limit=cantidad+1)
        aviso = await ctx.send(f'Se han eliminado {cantidad} mensajes por {ctx.author.mention}')
        await asyncio.sleep(15)
        await aviso.delete()

        channel=self.bot.get_channel(logchannel)
        embed=discord.Embed(title=f"{ctx.author} ha eliminado {cantidad} mensajes en {ctx.channel}", color=0xff0000)
        await channel.send(embed=embed)


    # Unban
    @commands.has_permissions(ban_members=True)
    @commands.command(name="Unban",aliases=["unban","desbanear","Desbanear","perdonar","Perdonar"])
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")
        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"{user.name}#{user.discriminator} ha sido desbaneado")
                return

        await ctx.send("Usuario no baneado / Usuario no encontrado.")




def setup(bot):
    bot.add_cog(Moderacion(bot))
