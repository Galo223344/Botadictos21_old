import discord
import asyncio
from datetime import datetime
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
            embed=discord.Embed(title="¡Usuario no valido!", description="", color=0xff0000)
            embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        if reason == None:
            reason = "La razón no ha sido especificada."

        embed=discord.Embed(title=f"Has sido baneado de {ctx.guild.name} por la siguiente razón:", description=reason, color=0x008080)
        embed.add_field(name="Puedes apelar al baneo aquí:", value="Haz [click aquí](https://gtadictos21.com/apelacion-ban) para rellenar el formulario de apelaciones.", inline=True)
        embed.set_footer(text=f"Baneo efectuado por: {ctx.message.author}", icon_url=ctx.author.avatar_url)
        
        try:
            await member.send(embed=embed)
        except:
            pass
        
        reason = reason + f"\nBaneo efectuado por {ctx.message.author}"

        await ctx.guild.ban(member, reason=reason)
        embed=discord.Embed(title=f"¡El usuario {member} ha sido baneado!", description="", color=0x008080)
        embed.set_footer(text=f"Baneo efectuado por: {ctx.message.author.name}", icon_url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embed)


    @ban.error
    async def handler_ban(self, ctx,error):
        if isinstance(error, discord.ext.commands.errors.UserNotFound):
            embed=discord.Embed(title="¡Usuario no valido!", description="", color=0xff0000)
            embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title="¡No tienes permisos para utilizar este comando!", description="Necesitas contar con el permiso `BAN_MEMBERS`", color=0xff0000)
            embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    # Kick

    @commands.command(name='kick', help='kickea a un miembro. Solo admins', aliases=["Kick","expulsar","Expulsar"])
    @commands.has_permissions(kick_members=True)
    async def kick (self, ctx, member:discord.Member=None, *,reason=None):
        if member == None or member == ctx.message.author:
            embed=discord.Embed(title="¡Usuario no valido!", description="", color=0xff0000)
            embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed=embed)
            return
        if reason == None:
            reason = "La razón no ha sido especificada."
        embed=discord.Embed(title=f"Has sido expulsado de {ctx.guild.name} por la siguiente razón:", description=f"{reason}", color=0x008080)
        embed.set_footer(text=f"Kick efectuado por: {ctx.message.author}", icon_url=ctx.author.avatar_url)
        await member.send(embed=embed)

        try:
            await member.send(message)
        except:
            pass
        await ctx.guild.kick(member, reason=reason)
        embed=discord.Embed(title=f"¡El usuario {member} ha sido expulsado!", description="", color=0x008080)
        embed.set_footer(text=f"Kick efectuado por: {ctx.message.author.name}", icon_url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embed)


        channel=self.bot.get_channel(logchannel)
        embed=discord.Embed(title=f"El usuario {member} ha sido expulsado por la siguiente razón: {reason}", description=f"El moderador/administrador {ctx.author.mention} ha expulsado a {member.mention}.", timestamp= datetime.now(), color=0x008080)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"ID del usuario: {member.id}") 
        await channel.send(embed=embed)

    @kick.error
    async def handler_kick(self, ctx,error):
        if isinstance(error, discord.ext.commands.errors.UserNotFound):
            embed=discord.Embed(title="¡Usuario no valido!", description="", color=0xff0000)
            embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            
        elif isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title="¡No tienes permisos para utilizar este comando!", description="Necesitas contar con el permiso `KICK_MEMBERS`", color=0xff0000)
            embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)            

    # Silenciar

    @commands.command(name='silenciar',help='Silencia al usuario especificado', aliases=["Silenciar","mute","Mute"])
    @commands.has_permissions(manage_roles=True)
    async def silenciar(self, ctx, member:discord.Member=None, *,reason=None):
        Role = discord.utils.get(member.guild.roles, name="Silenciado")
        role2 = discord.utils.get(member.guild.roles, name="La People👤")

        if member == None or member == ctx.message.author:
            embed=discord.Embed(title="¡Usuario no valido!", description="", color=0xff0000)
            embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed=embed)
            return
        if reason == None:
            reason = "La razón no ha sido especificada."
        if Role in member.roles:
            embed=discord.Embed(title=f"¡El usuario {member} ya se encuentra silenciado!", description="", color=0xff0000)
            embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return

        Role = discord.utils.get(member.guild.roles, name="Silenciado")
        await member.add_roles(Role)
        embed=discord.Embed(title=f"¡El usuario {member} ha sido silenciado!", description="", color=0x008080)
        embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        await member.remove_roles(role2)

        channel = self.bot.get_channel(logchannel)
        embed=discord.Embed(title="Un usuario ha sido muteado:", timestamp= datetime.now(), color=0xff0000)
        embed.add_field(name= "Usuario muteado:" ,value=member.mention, inline=False)
        embed.add_field(name= "Muteado por:" ,value=ctx.message.author.mention, inline=False)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"ID del usuario: {member.id}") 
        await channel.send(embed=embed)

    @silenciar.error
    async def handler_mute(self, ctx,error):
        if isinstance(error, discord.ext.commands.errors.UserNotFound):
            embed=discord.Embed(title="¡Usuario no valido!", description="", color=0xff0000)
            embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            
        elif isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title="¡No tienes permisos para utilizar este comando!", description="Necesitas contar con el permiso `MUTE_MEMBERS`", color=0xff0000)
            embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)            

    # Des-Silenciar/Unmute

    @commands.command(name='reactivar',help='Le saca el silencio al usuario especificado', aliases=["dessilenciar","unmute","Reactivar","Unmute","Dessilenciar","DesSilenciar"])
    @commands.has_permissions(manage_roles=True)
    async def reactivar(self, ctx, member:discord.Member=None):
        Role = discord.utils.get(member.guild.roles, name="Silenciado")

        if member == None or member == ctx.message.author:
            embed=discord.Embed(title="¡Usuario no valido!", description="", color=0xff0000)
            embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        if Role not in member.roles:
            embed=discord.Embed(title=f"¡El usuario {member} no se encuentra silenciado!", description="", color=0xff0000)
            embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed=embed)
            return

        Role = discord.utils.get(member.guild.roles, name="Silenciado")
        role2 = discord.utils.get(member.guild.roles, name="La People👤")

        await member.remove_roles(Role)
        embed=discord.Embed(title=f"¡El usuario {member} ha sido desmuteado!", description="", color=0x008080)
        embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        await member.add_roles(role2)

        channel = self.bot.get_channel(logchannel)
        embed=discord.Embed(title="Un usuario ha sido desmuteado", timestamp= datetime.now(), color=0x2bff00)
        embed.add_field(name= "Usuario desmuteado:" ,value=member.mention, inline=False)
        embed.add_field(name= "Desmuteado por:" ,value=ctx.message.author.mention, inline=False)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"ID del usuario: {member.id}")
        await channel.send(embed=embed)

    @reactivar.error
    async def handler_unmute(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.UserNotFound):
            embed=discord.Embed(title="¡Usuario no valido!", description="", color=0xff0000)
            embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title="¡No tienes permisos para utilizar este comando!", description="Necesitas contar con el permiso `MANAGE_ROLES`", color=0xff0000)
            embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)            

    # Purgar

    @commands.command(name='purgar',help='Purga \'x\' cantidad de mensajes', aliases=["Purgar","purge","Purge","prune","Prune","eliminar","Eliminar"])
    @commands.has_permissions(manage_guild=True)
    async def purge(self, ctx,cantidad : int):
        if cantidad <= 0:
            await ctx.send("._.")
            return
        if cantidad > 500:
            embed=discord.Embed(title="¡Se ha excedido el limite de 500 mensajes!", description="", color=0xff0000)
            embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        await ctx.channel.purge(limit=cantidad+1)
        aviso = await ctx.send(f'Se han eliminado {cantidad} mensaje(s) por {ctx.author.mention}')

        channel=self.bot.get_channel(logchannel)
        embed=discord.Embed(title=f"Un moderador/administrador ha utilizado el comando '!purge':", description=f"{ctx.author.mention} ha eliminado {cantidad} mensaje(s) en el canal \"{ctx.channel}\".", timestamp= datetime.now(), color=0xff0000)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text=f"ID del usuario: {ctx.author.id}") 
        await channel.send(embed=embed)
        await asyncio.sleep(15)
        await aviso.delete()
        
    @purge.error            
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title="¡No tienes permisos para utilizar este comando!", description="Necesitas contar con el permiso `MANAGE_GUILD`", color=0xff0000)
            embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)      

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
                embed=discord.Embed(title=f"¡El usuario {user.name}#{user.discriminator} ha sido desbaneado!", description="", color=0x008080)
                embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)

                channel = self.bot.get_channel(logchannel)
                embed=discord.Embed(title="Un usuario ha sido desbaneado", timestamp= datetime.now(), color=0x2bff00)
                embed.add_field(name= "Usuario desbaneado:" ,value=user.mention, inline=False)
                embed.add_field(name= "Desbaneado por:" ,value=ctx.message.author.mention, inline=False)
                embed.set_thumbnail(url=user.avatar_url)
                embed.set_footer(text=f"ID del usuario: {user.id}")
                await channel.send(embed=embed)
                return

        embed=discord.Embed(title="¡Usuario no baneado / Usuario no encontrado!", description="", color=0xff0000)
        embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        
    @unban.error            
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title="¡No tienes permisos para utilizar este comando!", description="Necesitas contar con el permiso `BAN_MEMBERS`", color=0xff0000)
            embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Moderacion(bot))
