import discord
import inspect
import io
import textwrap
import traceback
import aiohttp

from contextlib import redirect_stdout
from discord.ext import commands
from __main__ import admin_ids
from __main__ import logchannel

class EVAL(commands.Cog):
	def __init__(self,bot):
		self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print ("EVAL cog is ready")
    
    @commands.command(name='eval')
    async def _eval(self, ctx, *, body):
        """Evalua el codigo en python"""
        blocked_words = ['.delete()', 'os', 'subprocess', 'history()', '("token")', "('token')"]
        if ctx.author.id not in admin_ids:
            embed=discord.Embed(title="¡No tienes permisos para utilizar este comando!", description="Necesitas contar con el permiso `BOT_OPERATOR`", color=0xff0000)
            embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
            
        for x in blocked_words:
            if x in body:
                embed=discord.Embed(title="¡El comando contiene palabras bloqueads!", description=f"Por razones de seguridad, el comando `{x}` está bloqueado.", color=0xff0000)
                embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return 

        env = {
            'ctx': ctx,
            'bot': self.bot,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            'source': inspect.getsource
        }

        def cleanup_code(content):
            """Automaticamente elimina los bloques de codigo"""
            if content.startswith('```') and content.endswith('```'):
                return '\n'.join(content.split('\n')[1:-1])

            return content.strip('` \n')

        env.update(globals())

        body = cleanup_code(body)
        stdout = io.StringIO()
        err = out = None

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        def paginate(text: str):
            '''Generador simple que crea paginas de texto'''
            last = 0
            pages = []
            for curr in range(0, len(text)):
                if curr % 1980 == 0:
                    pages.append(text[last:curr])
                    last = curr
                    appd_index = curr
            if appd_index != len(text)-1:
                pages.append(text[last:curr])
            return list(filter(lambda a: a != '', pages))
        
        try:
            exec(to_compile, env)
        except Exception as e:
            err = await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
            return await ctx.message.add_reaction('\u2049')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            err = await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            if ret is None:
                if value:
                    try:
                        
                        out = await ctx.send(f'```py\n{value}\n```')
                    except:
                        paginated_text = paginate(value)
                        for page in paginated_text:
                            if page == paginated_text[-1]:
                                out = await ctx.send(f'```py\n{page}\n```')
                                break
                            await ctx.send(f'```py\n{page}\n```')
            else:
                try:
                    out = await ctx.send(f'```py\n{value}{ret}\n```')
                except:
                    paginated_text = paginate(f"{value}{ret}")
                    for page in paginated_text:
                        if page == paginated_text[-1]:
                            out = await ctx.send(f'```py\n{page}\n```')
                            break
                        await ctx.send(f'```py\n{page}\n```')

        if out:
            await ctx.message.add_reaction('\u2705')  
        elif err:
            await ctx.message.add_reaction('\u2049')  
        else:
            await ctx.message.add_reaction('\u2705')

    channel=bot.get_channel(logchannel)
    embed=discord.Embed(title=f"Un operador ha utilizado el comando `!eval`", description=f"El operador {ctx.author.mention} ha utilizado el comando eval en el canal: {ctx.message.channel}", timestamp= datetime.now(), color=0xff7d00)
    embed.set_thumbnail(url=ctx.author.avatar_url)
    embed.set_footer(text=f"ID del usuario: {ctx.author.id}")
    await channel.send(embed=embed)

    @eval.error
    async def eval_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            embed=discord.Embed(title="¡Argumento invalido!", description="", color=0xff0000)
            embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(EVAL(bot))