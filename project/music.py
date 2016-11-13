from __future__ import unicode_literals
import urllib.request
import urllib.parse
import youtube_dl
import re
import os
from pprint import pprint
import telepot

telegramtoken = '275419906:AAEQ_fAAy3dMWnqoSiJBFmYnc_CC28nh9Fg'

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'photo':
        bot.download_file(msg['photo'][-1]['file_id'], 'img/file.png')

    elif content_type == 'text':
        pprint(msg['from']['id'])
        pprint
        text = msg['text']

        match = re.search('\/(\S*) *(.*)', text)
        try:
            command = str(match.group(1)).lower()

            arg = str(match.group(2))
            print(command)
            print(arg)
            print("\n")
        except:
            print(text)
            return

        if command == 'song':
            MyDirectory = os.listdir('/opt/app-root/src/project')
            for file in MyDirectory:
                if file.endswith('.mp3'):
                    os.remove(file)
            query_string = urllib.parse.urlencode({"search_query": arg})
            html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
            search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download(["http://www.youtube.com/watch?v=" + search_results[0]])
                MyDirectory = os.listdir('/opt/app-root/src/project')
                for file in MyDirectory:
                    if file.endswith('.mp3'):
                        print (file)
                        bot.sendAudio(chat_id, open(file,'rb'))
                        break
        elif command == "help":
            helpstring = """
            Just write the song you want and wait for its arrival
   """
            bot.sendMessage(chat_id, helpstring)




            if command == 'ex':
                exec(arg)

            elif command == 'sys':
                ret = os.popen(arg).read()
                bot.sendMessage(chat_id, str(ret))

bot = telepot.Bot(telegramtoken)
bot.message_loop(handle)
print(bot.getMe())

from time import sleep

while 1:
    sleep(10)