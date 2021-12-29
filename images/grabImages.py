import win32com.client
import os, time

dictionary = {}

run = True
i = 0
while run:
    o = win32com.client.gencache.EnsureDispatch("iTunes.Application") #connect to the COM of iTunes.Application
    i += 1
    path = (os.path.dirname(os.path.realpath(__file__))).replace("\\", "\\\\") + "\\" + str(i) + ".png"

    artwork = o.CurrentTrack.Artwork.Item(1).SaveArtworkToFile(path)

    track = o.CurrentTrack.Name
    artist = o.CurrentTrack.Artist

    key = track + ":" + artist
    dictionary[key] = i

    print(key)
    print("sleeping 5 seconds")
    time.sleep(5)
    if i == 33:
        run = False
    
print(dictionary)

f = open("dict", "w")
f.write(str(dictionary))
f.close()