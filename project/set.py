import json
import os
import shutil
import configparser
import time

import LowerUtils as lu
import guilded
import yts

from pygame._sdl2 import get_num_audio_devices, get_audio_device_name
from pygame import mixer
import sounddevice as sd
import soundfile as sf

from pytube import YouTube
from pydub import AudioSegment
from youtube_search import YoutubeSearch

config = configparser.ConfigParser()
config.read('./project/config.ini')

mic = config['DEV']['mic']
sound_api = config['DEV']['api']


pre = config['GUILDED']['prefix']
own = config['GUILDED']['owner']

bot = guilded.Bot(command_prefix= pre, owner_id=own)

state = 0

class YTH:

    @staticmethod
    def check(title):
        if f"{title}.wav" in os.listdir("./waves/") or f"{title}.mp4" in os.listdir("./mp3/") or f"{title}.mp3" in os.listdir("./mp3/"):
            if f"{title}.wav" in os.listdir("./waves/"):
                return False
            elif  f"{title}.mp4" in os.listdir("./mp3/"):
                utilities.convertToWav(f"./mp3/{title}.mp4")
                return False
            elif  f"{title}.mp3" in os.listdir("./mp3/"):
                utilities.convertToWav(f"./mp3/{title}.mp3")
                return False
        else:
            return True

    @staticmethod
    def download(link):
        vid = YouTube(link)
        title = lu.characterRemover(vid.title)
        if YTH.check(title):
            yt_video = vid.streams.filter(only_audio = True, adaptive= True).first()
            yt_video.download(f"./mp3/", filename = f"{title}")
            utilities.convertToWav(f"./mp3/{title}.mp4")

class utilities:

    @staticmethod
    def getDevice():
        mixer.init()
        devices = [get_audio_device_name(x, 0).decode() for x in range(get_num_audio_devices(0))]
        print (devices)
        if mic in devices:
            mixer.quit()
            return True
        else:
            print('OOF Device not found.')
            mixer.quit()
            return False
    
    @staticmethod
    def convertToWav(file):
        revfilename = file[::-1]
        revext = revfilename[0:3]
        ext = revext[::-1]
        if  ext == "mp3":
            sound = AudioSegment.from_file(file, format = "mp3")
            sound.export(f"{file[0:-4]}.wav", format="wav")
            shutil.move(f"{file[0:-4]}.wav", "./waves/")
            return
        elif ext == "mp4":
            sound = AudioSegment.from_file(file, format = "mp4")
            sound.export(f"{file[0:-4]}.wav", format="wav")
            shutil.move(f"{file[0:-4]}.wav", "./waves/")
            return

class playAudio:
    @staticmethod
    async def  playMeg(link, vid):
        title = lu.characterRemover(vid.title)
        global state
        if f"{title}.wav" in os.listdir("./waves/"):
            fn = f"./waves/{title}.wav"
            data, fs = sf.read(fn, dtype='float32')  
            sd.play(data, fs, device = f"{mic}, {sound_api}")
            state = 1
            status = sd.wait()
            state = 0
        else:
            YTH.download(link)
            fn = f"./waves/{title}.wav"
            data, fs = sf.read(fn, dtype='float32')  
            sd.play(data, fs, device = f"{mic}, {sound_api}")
            state = 1
            status = sd.wait()
            state = 0

    @staticmethod
    def play(wav):
        if wav.split('/')[-1] in os.listdir('./waves/'):
            data, fs = sf.read(wav, dtype='float32')  
            sd.play(data, fs, device = f"{mic}, {sound_api}")
            status = sd.wait()
        else:
            print('Specified file did not exist')

@bot.event()
async def on_ready():
    print('Comrade I have logged in as:' + bot.user.name)

@bot.command()
async def play(ctx):
    if state != 1:
        songname = ctx.content.replace(f'{pre}play', '')
        embed = guilded.Embed(title="Muzach", description=f"Yay les go playing ur spicy muzach")
        link = str(yts.searchVid(songname))
        vid = YouTube(link)
        title = lu.characterRemover(vid.title)
        embed.add_field(name=f"Searched for, {songname}", value=f"Got song, {title}, from YT with link, {link}")
        embed.set_thumbnail(ctx.author.avatar_url.replace('https://img.guildedcdn.com/','https://s3-us-west-2.amazonaws.com/www.guilded.gg/'))
        await ctx.send(embed=embed)
        await playAudio.playMeg(link, vid)
    else:
        embed = guilded.Embed(title="Something is playing currently", description=f"Wait for your turn pls")
        embed.set_thumbnail(ctx.author.avatar_url.replace('https://img.guildedcdn.com/','https://s3-us-west-2.amazonaws.com/www.guilded.gg/'))
        await ctx.send(embed=embed)

bot.run(config['GUILDED']['user'], config['GUILDED']['pass'])
