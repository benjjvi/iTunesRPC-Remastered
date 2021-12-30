# encoding: utf-8
import win32com.client
import os, time

o = win32com.client.gencache.EnsureDispatch("iTunes.Application") #connect to the COM of iTunes.Application

try:
    f = open("dict", "r", encoding="utf-8")
    dictionary = eval(f.read())
    f.close()
except Exception:
    dictionary = {}

run = True
i = int(input("Start from what number? This will be the number that the first image is saved as e.g entering 34 will save 34.png\n> "))
to = int(input("Continue counting untill what number?\n> "))

print("Starting to collect data in 10 seconds. Be prepared.")
time.sleep(10)

while run:
    print("Getting first item.")
    path = (os.path.dirname(os.path.realpath(__file__))).replace("\\", "\\\\") + "\\" + str(i) + ".png"
    artwork = o.CurrentTrack.Artwork.Item(1).SaveArtworkToFile(path)

    track = o.CurrentTrack.Name
    artist = o.CurrentTrack.Artist
    key = track + ":" + artist
    dictionary[key] = i

    print("Saved "+ track +" by "+ artist +" with dictionary key "+ key +" with value "+ str(i))
    i += 1
    time.sleep(4)
    if i == to:
        run = False
    

f = open("dict", "w", encoding="utf-8")
f.write(str(dictionary))
f.close()

print("Completed! Please copy the file named 'dict' to the iTunesRPC-Remastered folder.")