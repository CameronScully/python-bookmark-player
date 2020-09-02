"""
bugs
- soundcloud breaks player
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import numpy as np
import random
import time
import msvcrt
from colorama import Fore, Back, Style, init

init()

class Folder:
    def __init__(self, name, songs):
        self.name = name
        self.songs = songs

class Song:
    def __init__(self, name, link):
        self.name = name
        self.link = link


cwd = os.getcwd()

chrome_options = Options()
chrome_options.add_extension(cwd+'/adblock.crx')

browser = webdriver.Chrome(chrome_options=chrome_options)

#go to bookmarks file
browser.get(cwd+'/bookmarks_28_08_2020.html')

#find music fold in bookmarks
music_folder = browser.find_elements_by_xpath('/html/body/dl/dt/dl/dt[15]/dl/dt')

#initilize array for folder order
folder_order = [None] * len(music_folder)

#populate folder order
for i in range(0, len(folder_order)):
    folder_order[i] = i

#randomise folder order
random.shuffle(folder_order)

que = []

#for ever folder -> record the folder name
for i in range(0, len(folder_order)):
    #get all songs in folder
    #songs = music_folder[folder_order[i]].find_elements_by_xpath("./dl/dt/a")
    folder = Folder(music_folder[folder_order[i]].find_element_by_xpath("./h3").text, music_folder[folder_order[i]].find_elements_by_xpath("./dl/dt/a"))

    #add all songs from folder to que
    que.append(folder)

    #randomize song order
    random.shuffle(que[i].songs)

#now play a song from each folder and remove them
up_next = []
index = 0

#while there are still unplayed folders
while len(que) > 0:
    #loop folders untill empty
    if(index >= len(que)):
        index = 0

    #if there are still unplayed songs
    if(len(que[index].songs) > 0):

        #add to up next
        song = Song(que[index].songs[0].text, que[index].songs[0].get_attribute('href'))

        up_next.append(song)

        #and remove it from the que
        que[index].songs.pop(0)

        #and remove this folder if empty
        if(len(que[index].songs) == 0):
            que.pop(index)
    
    index = index+1
    
#----------------------------------
#Need to check here if the video has stops
#Need to check if the video has been taken down
#----------------------------------


browser.get(up_next[0].link)

if up_next[0].link.find("youtube") != -1:
    print(Fore.GREEN,0,"/",len(up_next),up_next[0].name)
else:
    print(Fore.RED,0,"/",len(up_next),up_next[0].name)

if up_next[1].link.find("youtube") != -1:
    print(Fore.GREEN,1,"/",len(up_next),up_next[1].name)
else:
    print(Fore.RED,1,"/",len(up_next),up_next[1].name)

#play every time the user hits enter
for i in range(1, len(up_next)):
    try:
        while True:
            state = browser.execute_script('return document.getElementById("movie_player").getPlayerState();')
            if state == 0:
                break
            elif state == -1:
                break

            if msvcrt.kbhit():
                if msvcrt.getwche() == '\r':
                    break

            time.sleep(0.1)

        if up_next[i+1].link.find("youtube") != -1:
            browser.get(up_next[i].link)
            print(Fore.GREEN,i+1,"/",len(up_next),up_next[i+1].name)
        else:
            print(Fore.RED,i+1,"/",len(up_next),up_next[i+1].name)
        
    except Exception as e:
        print(e)

    