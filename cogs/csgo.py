from discord.ext import commands
import discord

class CSGO(commands.Cog):
	def __init__(self,bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print ("CSGO cog is ready")	

	@commands.command(name="csgo", aliases=["CSGO","Counter","counter","Conter","conter"])
	async def ciesgou(self,ctx,*,arg=None):
			embed=discord.Embed(title="¡Te envié los datos por mensaje privado! (Asegurate de tener los mensajes privados habilitados)", description="", color=ctx.author.color)
			embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
			await ctx.channel.send(embed=embed)
			await ctx.author.send("""
	**Reglas:** 

	1) Mantener el respeto entre los usuarios. NO se tolera ningún tipo de xenofobia, racismo, etc.
	2) Es un servidor para jugar entre todos de forma amistosa, no lo arruines.
	3) Está **terminantemente prohibido** el uso de cheats (El **VAC** se encuentra activado).
	4) Ante cualquier consulta, problema o duda, contacta a un Moderador o Administrador.
	5) Si querés invitar a tus amigos, invitalos primero al discord (Gtadictos21.com/discord) y luego al servidor.
	6) GLHF!

	Para conectarse, escribe en la consola: `connect csgo.gtadictos21.com`
	""")



def setup(bot):
	bot.add_cog(CSGO(bot))

