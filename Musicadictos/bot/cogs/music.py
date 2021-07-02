import asyncio
import datetime as dt
import random
import re
import typing as t
import os
from enum import Enum

import discord
import wavelink
from discord.ext import commands
from dotenv import load_dotenv

######### Importado por Galovich
import requests
from PIL import Image
import traceback
from fast_colorthief import get_dominant_color as getCol
import tekore as tk


# Cargamos el .env con los tokens
load_dotenv()
SP_ID = os.getenv('SP_ID')
SP_SECRET = os.getenv('SP_SECRET')

app_token = tk.request_client_token(SP_ID, SP_SECRET)
spotify = tk.Spotify(app_token)

URL_REGEX = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
OPTIONS = {
    "1️⃣": 0,
    "2⃣": 1,
    "3⃣": 2,
    "4⃣": 3,
    "5⃣": 4,
}


class AlreadyConnectedToChannel(commands.CommandError):
    pass


class NoVoiceChannel(commands.CommandError):
    pass


class QueueIsEmpty(commands.CommandError):
    pass


class NoTracksFound(commands.CommandError):
    pass


class PlayerIsAlreadyPaused(commands.CommandError):
    pass


class NoMoreTracks(commands.CommandError):
    pass


class NoPreviousTracks(commands.CommandError):
    pass


class InvalidRepeatMode(commands.CommandError):
    pass


class RepeatMode(Enum):
    NONE = 0
    ONE = 1
    ALL = 2


class Queue:
    def __init__(self):
        self._queue = []
        self.position = 0
        self.repeat_mode = RepeatMode.NONE

    @property
    def is_empty(self):
        return not self._queue

    @property
    def current_track(self):
        if not self._queue:
            raise QueueIsEmpty

        if self.position <= len(self._queue) - 1:
            return self._queue[self.position]

    @property
    def upcoming(self):
        if not self._queue:
            raise QueueIsEmpty

        return self._queue[self.position + 1:]

    @property
    def history(self):
        if not self._queue:
            raise QueueIsEmpty

        return self._queue[:self.position]

    @property
    def length(self):
        return len(self._queue)

    def add(self, *args):
        self._queue.extend(args)

    def get_next_track(self):
        if not self._queue:
            raise QueueIsEmpty

        self.position += 1

        if self.position < 0:
            return None
        elif self.position > len(self._queue) - 1:
            if self.repeat_mode == RepeatMode.ALL:
                self.position = 0
            else:
                return None

        return self._queue[self.position]

    def shuffle(self):
        if not self._queue:
            raise QueueIsEmpty

        upcoming = self.upcoming
        random.shuffle(upcoming)
        self._queue = self._queue[:self.position + 1]
        self._queue.extend(upcoming)

    def set_repeat_mode(self, mode):
        if mode == "none":
            self.repeat_mode = RepeatMode.NONE
        elif mode == "1":
            self.repeat_mode = RepeatMode.ONE
        elif mode == "all":
            self.repeat_mode = RepeatMode.ALL

    def empty(self):
        self._queue.clear()
        self.position = 0


class Player(wavelink.Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = Queue()

    async def connect(self, ctx, channel=None):
        if self.is_connected:
            raise AlreadyConnectedToChannel

        if (channel := getattr(ctx.author.voice, "channel", channel)) is None:
            raise NoVoiceChannel

        await super().connect(channel.id)
        return channel

    async def teardown(self):
        try:
            await self.destroy()
        except KeyError:
            pass

    async def sacarColor(self,track):

        if not os.path.isfile(f"./cache/thumb_{track.ytid}.jpeg"):

            resoluciones = ["maxresdefault","hqdefault","mqdefault","sddefault"]

            for resolucion in resoluciones:
                imagen = requests.get(f"https://i3.ytimg.com/vi/{track.ytid}/{resolucion}.jpg",stream=True)
                imagen.raw.decode_content = True

                im = Image.open(imagen.raw)
                width, height = im.size   # Get dimensions
                if width == 120 and height == 90:
                    continue
                left = (width - width/1.8)/2
                top = (height - width/1.8)/2
                right = (width + width/1.8)/2
                bottom = (height + width/1.8)/2
                break

            # Crop the center of the image
            im = im.crop((left, top, right, bottom))

            im.save(f"./cache/thumb_{track.ytid}.jpeg")

        colores = getCol(f"./cache/thumb_{track.ytid}.jpeg",quality=3)
        coulores = discord.Colour.from_rgb(colores[0],colores[1],colores[2])

        return coulores


    async def add_tracks(self, ctx, src, tracks):
        if not tracks:
            raise NoTracksFound

        elif src == "sp_p":
            # await ctx.send("Recibidas canciones, canciones recibidas:")
            for cancion in tracks[0]:
                self.queue.add(cancion)

            formateado = ""
            if len(tracks[1]) >4:
                for cancion in tracks[1][:4]:
                    formateado = formateado+f"\'{cancion}\'"+"\n"
                formateado = formateado + f"Y {len(tracks[1])-4} canciónes mas..."
            else:
                for cancion in tracks[1]:
                    formateado = formateado+f"\'{cancion}\'"+"\n"

            colorcito = await self.sacarColor(tracks[0][0])

            embed = discord.Embed(title="Canciónes agregadas a la lista:",description=f"**{formateado}**",color=colorcito)
            file = discord.File(f"./cache/thumb_{tracks[0][0].ytid}.jpeg", filename=f"{tracks[0][0].ytid}.jpeg")
            tracks[0][0].thumb = f"attachment://{tracks[0][0].ytid}.jpeg"
            embed.set_thumbnail(url=tracks[0][0].thumb)
            embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            # await ctx.send(file=file)
            await ctx.send(file=file,embed=embed)

        elif src == "sp_t":
            self.queue.add(tracks[0])
            colorcito = await self.sacarColor(tracks[0])
            embed = discord.Embed(title="Canción agregada la lista:",description=f"**{tracks[0].title}**",color=colorcito)
            file = discord.File(f"./cache/thumb_{tracks[0].ytid}.jpeg", filename=f"{tracks[0].ytid}.jpeg")
            tracks[0].thumb = f"attachment://{tracks[0].ytid}.jpeg"
            embed.set_thumbnail(url=tracks[0].thumb)
            embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            await ctx.send(file=file,embed=embed)



        elif isinstance(tracks, wavelink.TrackPlaylist):
            for cancion in tracks.tracks:
                cancion.thumb = f"https://i3.ytimg.com/vi/{cancion.ytid}/maxresdefault.jpg"
            self.queue.add(*tracks.tracks)
            musicas = set(i.title for i in tracks.tracks)
            musicas = list(musicas)
            
                    
            formateado = ""
            if len(musicas) >4:
                for cancion in musicas[:4]:
                    formateado = formateado+f"\'{cancion}\'"+"\n"
                formateado = formateado + f"Y {len(musicas)-4} canciónes mas..."
            else:
                for cancion in musicas:
                    formateado = formateado+f"\'{cancion}\'"+"\n"

            colorcito = await self.sacarColor(tracks.tracks[0])

            embed = discord.Embed(title="Canciónes agregadas a la lista:",description=f"**{formateado}**",color=colorcito)
            file = discord.File(f"./cache/thumb_{tracks.tracks[0].ytid}.jpeg", filename=f"{tracks.tracks[0].ytid}.jpeg")
            tracks.tracks[0].thumb = f"attachment://{tracks.tracks[0].ytid}.jpeg"
            embed.set_thumbnail(url=tracks.tracks[0].thumb)
            embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            # await ctx.send(file=file)
            await ctx.send(file=file,embed=embed)

        elif len(tracks) == 1:
            tracks[0].thumb = f"https://i3.ytimg.com/vi/{tracks[0].ytid}/maxresdefault.jpg"
            self.queue.add(tracks[0])
            colorcito = await self.sacarColor(tracks[0])
            embed = discord.Embed(title="Canción agregada la lista:",description=f"**{tracks[0].title}**",color=colorcito)
            file = discord.File(f"./cache/thumb_{tracks[0].ytid}.jpeg", filename=f"{tracks[0].ytid}.jpeg")
            tracks[0].thumb = f"attachment://{tracks[0].ytid}.jpeg"
            embed.set_thumbnail(url=tracks[0].thumb)
            embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            await ctx.send(file=file,embed=embed)


        else:
            if (track := await self.choose_track(ctx, tracks)) is not None:
                self.queue.add(track)

                track.thumb = f"https://i3.ytimg.com/vi/{track.ytid}/maxresdefault.jpg"

                colorcito = await self.sacarColor(track)

                embed = discord.Embed(title="Canción agregada la lista:",description=f"**{track.title}**",color=colorcito)
                file = discord.File(f"./cache/thumb_{track.ytid}.jpeg", filename=f"{track.ytid}.jpeg")
                track.thumb = f"attachment://{track.ytid}.jpeg"
                embed.set_thumbnail(url=track.thumb)
                embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
                await ctx.send(file=file, embed=embed)

                # await ctx.send(f"La cancion **{track.title}** fue añadida a la lista.")

        if not self.is_playing and not self.queue.is_empty:
            await self.start_playback()

    async def choose_track(self, ctx, tracks):
        def _check(r, u):
            return (
                r.emoji in OPTIONS.keys()
                and u == ctx.author
                and r.message.id == msg.id
            )

        embed = discord.Embed(
            title="¡Elige una canción!",
            description=(
                "\n".join(
                    f"**{i+1}.** {t.title} ({t.length//60000}:{str(t.length%60).zfill(2)})"
                    for i, t in enumerate(tracks[:5])
                )
            ),
            colour=ctx.author.colour,
            timestamp=dt.datetime.utcnow()
        )
        embed.set_author(name="Resultados de busqueda:")
        embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)

        msg = await ctx.send(embed=embed)
        for emoji in list(OPTIONS.keys())[:min(len(tracks), len(OPTIONS))]:
            await msg.add_reaction(emoji)

        try:
            reaction, _ = await self.bot.wait_for("reaction_add", timeout=60.0, check=_check)
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.message.delete()
        else:
            await msg.delete()
            return tracks[OPTIONS[reaction.emoji]]

    async def start_playback(self):
        await self.play(self.queue.current_track)

    async def advance(self):
        try:
            if (track := self.queue.get_next_track()) is not None:
                await self.play(track)
        except QueueIsEmpty:
            pass

    async def repeat_track(self):
        await self.play(self.queue.current_track)


class Music(commands.Cog, wavelink.WavelinkMixin):
    def __init__(self, bot):
        self.bot = bot
        self.wavelink = wavelink.Client(bot=bot)
        self.bot.loop.create_task(self.start_nodes())

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.bot and after.channel is None:
            if not [m for m in before.channel.members if not m.bot]:
                await self.get_player(member.guild).teardown()

    @wavelink.WavelinkMixin.listener()
    async def on_node_ready(self, node):
        print(f"El nodo de Wavelink `{node.identifier}` esta listo.")

    @wavelink.WavelinkMixin.listener("on_track_stuck")
    @wavelink.WavelinkMixin.listener("on_track_end")
    @wavelink.WavelinkMixin.listener("on_track_exception")
    async def on_player_stop(self, node, payload):
        if payload.player.queue.repeat_mode == RepeatMode.ONE:
            await payload.player.repeat_track()
        else:
            await payload.player.advance()

    async def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.DMChannel):
            await ctx.send("¡Los comandos para este bot no estan disponibles por mensajes privados!")
            return False

        return True

    async def start_nodes(self):
        await self.bot.wait_until_ready()

        nodes = {
            "MAIN": {
                "host": "127.0.0.1",
                "port": 2333,
                "rest_uri": "http://127.0.0.1:2333",
                "password": "youshallnotpass",
                "identifier": "MAIN",
                "region": "brazil",
            }
        }

        for node in nodes.values():
            await self.wavelink.initiate_node(**node)

    def get_player(self, obj):
        if isinstance(obj, commands.Context):
            return self.wavelink.get_player(obj.guild.id, cls=Player, context=obj)
        elif isinstance(obj, discord.Guild):
            return self.wavelink.get_player(obj.id, cls=Player)

    @commands.command(name="conectar", aliases=["unirse","connect"])
    async def connect_command(self, ctx, *, channel: t.Optional[discord.VoiceChannel]):
        player = self.get_player(ctx)
        channel = await player.connect(ctx, channel)
        await ctx.send(f"Conectado a {channel.name}.")

    @connect_command.error
    async def connect_command_error(self, ctx, exc):
        if isinstance(exc, AlreadyConnectedToChannel):
            await ctx.send("¡El bot ya se encuentra en un canal de voz!")
        elif isinstance(exc, NoVoiceChannel):
            await ctx.send("¡No se encontró un canal al cual unirse!")

    @commands.command(name="desconectar", aliases=["disconnect","d"])
    async def disconnect_command(self, ctx):
        player = self.get_player(ctx)
        await player.teardown()
        await ctx.send("El bot se desconectó")

    @commands.command(name="play", aliases=["p"])
    async def play_command(self, ctx, *, query: t.Optional[str]):
        player = self.get_player(ctx)
        # print(query)

        if not player.is_connected:
            await player.connect(ctx)

        if query is None:
            if player.queue.is_empty:
                raise QueueIsEmpty

            await player.set_pause(False)
            await ctx.send("Resumido...")

        elif "open.spotify.com" in str(query):
            await ctx.channel.send("Para reproducir de Spotify por favor usá !spotify [link] ó !sp [link]")

        else:
            query = query.strip("<>")
            if not re.match(URL_REGEX, query):
                query = f"ytsearch:{query}"

            await player.add_tracks(ctx,"yt",await self.wavelink.get_tracks(query))

    @play_command.error
    async def play_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("¡La lista de reproduccion se encuentra vacia!")
        elif isinstance(exc, NoVoiceChannel):
            await ctx.send("¡No se encontró un canal al cual unirse!")
        else:
            print(exc)
            print(traceback.format_exc())

    @commands.command(name="spotify",aliases=["sp"])
    async def spoti(self,ctx, *, query:t.Optional[str]):
        player = self.get_player(ctx)

        if not player.is_connected:
            await player.connect(ctx)

        if "open.spotify.com" in query:
            link = query.split("/")
            if "playlist" in link:
                await ctx.send("Procesando... ⚙️")
                async with ctx.typing():
                    link = link[4].split("?")
                    link = link[0]
                    pl_id = link
                    # print(pl_id)

                    playlist = spotify.playlist_items(pl_id)
                    playlist = spotify.all_items(playlist)
                    musicas = list()
                    canciones = list()
                    for track in playlist:
                        if track.track == None:
                            continue
                        cancion_formateada = f"{track.track.name} - {track.track.album.artists[0].name}"
                        musicas.append(cancion_formateada)
                        cancion_objeto = await self.wavelink.get_tracks(f"ytsearch:{cancion_formateada} Audio")
                        cancion_objeto = cancion_objeto[0]
                        cancion_objeto.thumb = f"https://i3.ytimg.com/vi/{cancion_objeto.ytid}/maxresdefault.jpg"
                        canciones.append(cancion_objeto)

                await player.add_tracks(ctx,"sp_p",(canciones,musicas))


            elif "track" in link:
                link = link[4].split("?")
                link = link[0]
                track_id = link
                track = spotify.track(track_id)
                if track == None:
                    await ctx.send("Canción no disponible.")
                    return
                cancion_formateada = f"{track.name} - {track.album.artists[0].name}"
                cancion_objeto = await self.wavelink.get_tracks(f"ytsearch:{cancion_formateada} Audio")
                cancion_objeto = cancion_objeto[0]
                cancion_objeto.thumb = f"https://i3.ytimg.com/vi/{cancion_objeto.ytid}/maxresdefault.jpg"
                await player.add_tracks(ctx,"sp_t",(cancion_objeto,cancion_formateada))

    @spoti.error
    async def spoti_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("¡La lista de reproduccion se encuentra vacia!")
        elif isinstance(exc, NoVoiceChannel):
            await ctx.send("¡No se encontró un canal al cual unirse!")
        else:
            if "404: Not found." in str(exc):
                await ctx.send("Playlist no encontrada. ¡Asegurate de que sea pública!")
            elif "404: Invalid playlist Id" in str(exc):
                await ctx.send("¡Link de playlist invalido!")
            else:
                print(exc)
                print(traceback.format_exc())

    @commands.command(name="pausa")
    async def pause_command(self, ctx):
        player = self.get_player(ctx)

        if player.is_paused:
            raise PlayerIsAlreadyPaused

        await player.set_pause(True)
        await ctx.send("¡La canción se encuentra pausada!")

    @pause_command.error
    async def pause_command_error(self, ctx, exc):
        if isinstance(exc, PlayerIsAlreadyPaused):
            await ctx.send("¡Esta canción ya se encuentra pausada!")

    @commands.command(name="stop")
    async def stop_command(self, ctx):
        player = self.get_player(ctx)
        player.queue.empty()
        await player.stop()
        await ctx.send("La lista se ha parado")

    @commands.command(name="saltar", aliases=["skip","s"])
    async def next_command(self, ctx):
        player = self.get_player(ctx)

        if not player.queue.upcoming:
            raise NoMoreTracks

        cancion = player.queue.upcoming[0]

        colorcitos = await player.sacarColor(cancion)

        await player.stop()
        embed = discord.Embed(title="Reproduciendo la siguiente canción...",description=cancion.title,colour=colorcitos)
        file = discord.File(f"./cache/thumb_{cancion.ytid}.jpeg", filename=f"{cancion.ytid}.jpeg")
        embed.set_thumbnail(url=f"attachment://{cancion.ytid}.jpeg")
        embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file,embed=embed)
        # await ctx.send(f"Reproduciendo la siguiente cancion...\n**{player.queue.upcoming[0].title}**")

    @next_command.error
    async def next_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("¡La lista de reproduccion se encuentra vacia!")
        elif isinstance(exc, NoMoreTracks):
            await ctx.send("¡No hay canciónes en la lista de reproduccion!")
        else:
            print(exc)
            print(traceback.format_exc())

    @commands.command(name="anterior")
    async def previous_command(self, ctx):
        player = self.get_player(ctx)

        if not player.queue.history:
            raise NoPreviousTracks


        player.queue.position -= 2
        await player.stop()

        await ctx.send(f"Reproduciendo la cancion anterior...\n**{player.queue.current_track}**")

    @previous_command.error
    async def previous_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("¡La lista de reproduccion se encuentra vacia!")
        elif isinstance(exc, NoPreviousTracks):
            await ctx.send("¡No hay canciones en la lista de reproduccion!")

    @commands.command(name="mezclar",aliases=["aleatorizar","barajar","random","shuffle"])
    async def shuffle_command(self, ctx):
        player = self.get_player(ctx)
        player.queue.shuffle()
        await ctx.send("Cola aleatorizada.")

    @shuffle_command.error
    async def shuffle_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("La lista no se puede aleatorizar, porque se encuentra vacia")

    @commands.command(name="repetir", aliases=["Repeticion","repetición","loop"])
    async def repeat_command(self, ctx, mode: str = None):
        if mode == None:
            await ctx.send("Uso: !repetir [Modo]\nDonde modo puede ser \'none\' para no repetir ninguna canción, \'1\' para repetir la canción que se está reproduciendo y \'all\', para repetir la lista actual.")
            return

        if mode not in ("none", "1", "all"):
            raise InvalidRepeatMode

        player = self.get_player(ctx)
        player.queue.set_repeat_mode(mode)
        await ctx.send(f"El modo de repeticion se encuentra en el modo: {mode}")

    @commands.command(name="cola", aliases=["lista","queue","q"])
    async def queue_command(self, ctx, show: t.Optional[int] = 10):
        player = self.get_player(ctx)

        if player.queue.is_empty:
            raise QueueIsEmpty

        embed = discord.Embed(
            title="Lista de reproduccion:",
            description=f"Mostrando las proximas {show} canciónes",
            colour=ctx.author.colour,
            timestamp=dt.datetime.utcnow()
        )
        embed.set_author(name="Resultados de la lista de reproduccion")
        embed.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        embed.add_field(
            name="Actualmente escuchando:",
            value=getattr(player.queue.current_track, "title", "¡No hay canciónes sonando actualmente!"),
            inline=False
        )
        if upcoming := player.queue.upcoming:
            embed.add_field(
                name="Luego:",
                value="\n".join(t.title for t in upcoming[:show]),
                inline=False
            )

        msg = await ctx.send(embed=embed)

    @queue_command.error
    async def queue_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("¡La lista de reproduccion se encuentra vacia!")

# print(dir(Music))

def setup(bot):
    bot.add_cog(Music(bot))
