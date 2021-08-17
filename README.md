# Botadictos21:

## Bot creado por Galo para [El Club De Los 21's](https://gtadictos21.com/discord)

Youtube cog sacado de este [repositorio de Github](https://github.com/Amethyst93/Discord-YouTube-Notifier) y modificado por mi mismo (Convertido a cog, arreglo de bugs y otros cambios varios)

Levels cog sacado de este [thread de Stackoverflow](https://stackoverflow.com/questions/62042331/how-to-create-a-leveling-system-with-discord-py-with-python) (La cantidad de experiencia dada fue modificada, y se realizaron otros cambios varios)

Ranking cog sacado de este [thread de Stackoverflow](https://stackoverflow.com/questions/61996040/discord-py-rank-command) (Arreglo de bugs y estilizado)

**Sos libre de copiar, modificar y hacer lo que quieras con este código.**

## Instalar dependencias:
¡Este bot requiere Python3 version: 3.9.x, y pip!

```
pip install -r requirements.txt
```
## Iniciar el bot:

```
python3 Botadictos21.py
```

### Configuraciones:

1. Crear un archivo **.env** de la siguiente manera: `DISCORD_TOKEN = "TU_TOKEN_DE_DISCORD_VA_AQUÍ"`
2. Cambiar **admin_ids** por los IDs de las personas que querés que controlen el bot.
3. Cambiar los emojis customizados por tuyos o unos no customizados en los cogs.
4. Agregar tu propia clave API de youtube en **YTconfig.yml** (Las instrucciónes para conseguír esta clave están en el repositorio original, o simplemente podés borrar todo lo relacionado a YouTube.)
5. Cambiar el ID de la guild por el ID de TU servidor en **Botadictos21.py**, y en los cogs.
6. Agregar tu clave API (en el archivo **.env**) o eliminar el modulo de Pterodactyl en **Misc.py**.
7. Utilizando los comandos "!sugchannel", "!logchannel", "!gvchannel" y "!init" deberás configurar tu servidor.

# Musicadictos21:

## Bot creado por Julián para [El Club De Los 21's](https://gtadictos21.com/discord)

Código base sacado de el tutorial de [Carberra](https://github.com/Carberra/discord.py-music-tutorial) (Luego, fue modificado; se añadieron embeds, thumbnails, y demás.)

### Instalar dependencias:
¡Este bot requiere Python3 version: 3.9.x, y pip!

```
python3 -m pip install -U "discord.py[voice]"
```
```
pip install wavelink
```
```
pip install lavalink
```
```
git clone https://github.com/bedapisl/fast-colorthief.git
```
```
sudo apt-get install cmake #(DENTRO DE LA CARPETA DEL COLORTHIEF)
```
```
git submodule update --init --recursive #(DENTRO DE LA CARPETA DEL COLORTHIEF)
```
```
pip3 install . #(DENTRO DE LA CARPETA DEL COLORTHIEF)
```
Instalar un entorno Java, descargar y descomprimir OpenJDK 13.0.2, y por ultimo, mover el archivo Lavalink.jar y application.yml a ese directorio.

**Nota: Primero se debe ejecutar el servidor de Lavalink (```java -jar Lavalink.jar```), y luego el bot (```python3 launcher.py```), siempre en ese orden.**


# Proximos proyectos:
* Añadir SQlite y despreciar JSON.
* Mejorar configuración de IDs (IDs de guidl y de usuarios)
* Crear cog de FAQS
* Y mas...

Ultima actualización: 17/08/2021 por: Julián (Gtadictos21)
