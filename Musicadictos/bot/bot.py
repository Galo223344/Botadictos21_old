from pathlib import Path

import discord
from discord.ext import commands


class MusicBot(commands.Bot):
    def __init__(self):
        self._cogs = [p.stem for p in Path(".").glob("./bot/cogs/*.py")]
        super().__init__(command_prefix=self.prefix, case_insensitive=True)

    def setup(self):
        print("Corriendo el inicio...")

        for cog in self._cogs:
            self.load_extension(f"bot.cogs.{cog}")
            print(f" Loaded `{cog}` cog.")
        self.remove_command('help')

        print("Ininiciando bot.")

    def run(self):
        self.setup()

        with open("data/token.0", "r", encoding="utf-8") as f:
            TOKEN = f.read()

        print("Running bot...")
        super().run(TOKEN, reconnect=True)

    async def shutdown(self):
        print("Cerrando la conexion a Discord...")
        await super().close()

    async def close(self):
        print("Cerrando conexion por teclado...")
        await self.shutdown()

    async def on_connect(self):
        print(f" Conectado a Discord (latencia: {self.latency*1000:,.0f} ms).")

    async def on_resumed(self):
        print("Bot funcionando nuevamente.")

    async def on_disconnect(self):
        print("El bot se encuentra desconectado.")

    # async def on_error(self, err, *args, **kwargs):
    #     raise

    # async def on_command_error(self, ctx, exc):
    #     raise getattr(exc, "original", exc)

    async def on_ready(self):
        self.client_id = (await self.application_info()).id
        print("Bot funcionando.")

    async def prefix(self, bot, msg):
        return commands.when_mentioned_or("!")(bot, msg)

    async def process_commands(self, msg):
        ctx = await self.get_context(msg, cls=commands.Context)

        if ctx.command is not None:
            await self.invoke(ctx)

    async def on_message(self, msg):
        if not msg.author.bot:
            await self.process_commands(msg)
