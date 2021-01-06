from discord.ext import commands, tasks
import time
import asyncio
import sys
from cogs.YTImplementation import YouTuber
from cogs.YTconfig import Config


config = Config('cogs/YTconfig.yml')
youtubers = config.getYouTubersList() if (config.getYouTubersNr() != 0) else sys.exit()
if (config.getDiscordChannelNr() == 0): sys.exit()
id = ''
GOOGLE_API = config.getConnectionData()[0]
pingEveryXMinutes = config.getPingTime()
threads = []
processes = []

class Youtube(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

        # update.start(self)

    i = 0
    while i < config.getYouTubersNr():
        temp_list = []
        temp_list.append(config.getYouTubersList()[i]['name'])
        temp_list.append(id) if not config.getYouTubersList()[i]['channelID'] else temp_list.append(config.getYouTubersList()[i]['channelID'])
        temp_list.append(True) if not id else temp_list.append(False)
        temp_list.append('')
        threads.append(temp_list)
        i += 1

    i = 0

    while i < config.getYouTubersNr():
        processes.append(YouTuber(GOOGLE_API, threads[i][1], threads[i][2]))
        i += 1

    @tasks.loop(minutes= pingEveryXMinutes * 60)
    async def update(self):
        while True:
            try:
                waittime = pingEveryXMinutes * 60
                item = 0
                while item < config.getYouTubersNr():
                    data = processes[item].update()
                    # print('Checking for new videos from {}'.format(threads[item][0]))
                    if processes[item].isNewVideo():
                        # print('{} HAS UPLOADED A NEW VIDEO! PUSHING UPDATE ON DISCORD.'.format(threads[item][0]))
                        # print(config.getDiscordChannelNr())
                        for x in range (0, config.getDiscordChannelNr()):
                            # print("Entrado en for loop")
                            # print(x)
                            newvideo = config.getDiscordChannelList()[x]['New video'].format(threads[item][0]) + '\n{}'.format(processes[item].getVideoLink(processes[item].videosData[0][1]))
                            # print("Newvideo guardado")
                            newvideo = newvideo[1:]
                            # print(newvideo)
                            # print(int(config.getDiscordChannelList()[x]['channelID']))
                            channel = self.bot.get_channel((int(config.getDiscordChannelList()[x]['channelID'])))
                            # print(channel)
                            await channel.send(newvideo)
                            # print("Mensaje tratado de enviar")

                    item += 1
                    # print("For loop roto")
            except:
                pass
            while waittime > 0:
                mins, secs = divmod(waittime, 60)
                timeformat = '{:02d}:{:02d}'.format(mins, secs)
                sys.stdout.write('Rechecking in ' + str(timeformat) + '\r')
                waittime -= 1
                await asyncio.sleep(1)


    @commands.Cog.listener()
    async def on_ready(self):
        print('Youtube cog is ready')
        self.update.start()

def setup(bot):
    bot.add_cog(Youtube(bot))
