# encoding: utf-8
import win32com.client
import os, time
f = open("dict", "r", encoding="utf-8")
dictionary = eval(f.read())
f.close()

run = True
i = int(input("start from what number? this will be the number that the first image is saved as e.g entering 34 will save 34.png> "))
to = int(inpur("continue till what number? > "))
while run:
    o = win32com.client.gencache.EnsureDispatch("iTunes.Application") #connect to the COM of iTunes.Application
    path = (os.path.dirname(os.path.realpath(__file__))).replace("\\", "\\\\") + "\\" + str(i) + ".png"
    artwork = o.CurrentTrack.Artwork.Item(1).SaveArtworkToFile(path)

    track = o.CurrentTrack.Name
    artist = o.CurrentTrack.Artist
    key = track + ":" + artist
    dictionary[key] = i
    i += 1

    print(key)
    print("sleeping 4 seconds")
    time.sleep(4)
    if i == to:
        run = False
    
print(dictionary)

f = open("dict", "w", encoding="utf-8")
f.write(str(dictionary))
f.close()