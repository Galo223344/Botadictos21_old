import discord
from discord.ext import commands

class Ignorar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print ("Ignorar cog is ready")

    @commands.command(name="conectar", aliases=["unirse","connect"])
    async def connect_command(self,ctx):
        pass
    @commands.command(name="desconectar", aliases=["disconnect"])
    async def disconnect_command(self,ctx):
        pass
    @commands.command(name="play",aliases=["Reproducir"])
    async def play_command(self,ctx):
        pass
    @commands.command(name="pausa")
    async def pause_command(self,ctx):
        pass
    @commands.command(name="stop")
    async def stop_command(self,ctx):
        pass
    @commands.command(name="saltar", aliases=["skip","saltear"])
    async def next_command(self,ctx):
        pass
    @commands.command(name="anterior",aliases=["Volver","atras"])
    async def previous_command(self,ctx):
        pass
    @commands.command(name="mezclar",aliases=["aleatorizar","barajar","random"])
    async def shuffle_command(self,ctx):
        pass
    @commands.command(name="repetir", aliases=["Repeticion","repetición"])
    async def repeat_command(self,ctx):
        pass
    @commands.command(name="cola",aliases=["Lista","queue"])
    async def queue_command(self,ctx):
        pass


def setup(bot):
    bot.add_cog(Ignorar(bot))