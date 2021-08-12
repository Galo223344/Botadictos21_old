from discord.ext import commands
from __main__ import admin_ids
import discord


class Spamlist(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print ("Spamlist cog is ready")	


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
    bot.add_cog(Spamlist(bot))