import discord
from discord.ext import commands
import random

class Fun(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    global callate_r
    global callate
    global insultos_r
    global insultos
    global caritas
    callate_r=["callate","cerra el orto","cerra el culo","quien te pregunto"]
    insultos_r=["puta","trolo","conchudo","gil","tonto","estupido","tarado","imbecil","bot de ","hijo de ","puto","pelotudo","gei","gey","gay","culiao","culiado","cara de"]
    insultos=["Que dijiste gil?","Queri piliar quliao?!",":\'(","Heriste mis sentimientos","!tempmute 5m Por insultar al bot"]
    callate=["Callate vos >:(","Bueno T_T","Mirá que te baneo eh\n!ban","Ño >:)"]
    caritas=[":)",";)","uwu","owo"]

    @commands.Cog.listener()
    async def on_ready(self):
        print ("Fun cog is ready")


    @commands.Cog.listener()
    async def on_message(self, message):

    	if message.reference != None:
    		respuesta = await message.channel.fetch_message(message.reference.message_id)

    	for insulto in insultos_r:
    		if insulto in message.content.lower() and ((f"<@{self.bot.user.id}>" in message.content) or (message.reference != None and respuesta.author.id == self.bot.user.id)):
    			await message.reply(random.choice(insultos),mention_author=False)
    			return
    	for palabra in callate_r:
    		if palabra in message.content.lower() and ((f"<@{self.bot.user.id}>" in message.content) or (message.reference != None and respuesta.author.id == self.bot.user.id)):
    			await message.reply(random.choice(callate),mention_author=False)
    			return

    	if "no tengo amigos" in message.content.lower():
    		await message.reply(f"Yo puedo ser tu amigo {random.choice(caritas)}",mention_author=False)




def setup(bot):
    bot.add_cog(Fun(bot))
