# encoding: utf-8

import win32com.client
import os
import time
import ast

try:
    f = open("dict", "r", encoding="utf-8")
    dictionary = ast.literal_eval(f.read())
    f.close()
except Exception:
    dictionary = {}

run = True
i = (
    int(
        input(
            "Start from what number? This will be the number that the first image is saved as e.g entering 34 will save 34.png\n> "
        )
    )
    - 1
)
toval = (int(input("How many songs are there to count?\n> ")) + i) - 1

print("Getting songs in 3 seconds.")
time.sleep(3)
o = win32com.client.gencache.EnsureDispatch(
    "iTunes.Application"
)  # connect to the COM of iTunes.Application

while run:
    i += 1
    path = (os.path.dirname(os.path.realpath(__file__))) + "\\" + str(i) + ".png"

    if path[:2] == r"\\":
        print("You are running on a network server.")
        print("Please use a local folder.")

    artwork = o.CurrentTrack.Artwork.Item(1).SaveArtworkToFile(path)
    # win32com.client.CastTo(o.CurrentTrack.Artwork.Item(1).SaveArtworkToFile(path), 'IITFileOrCDTrack')

    track = o.CurrentTrack.Name
    artist = o.CurrentTrack.Artist

    key = track + ":" + artist
    dictionary[key] = i

    print("Got artwork for " + key + " with value " + str(i))
    if i >= toval:
        run = False
    else:
        time.sleep(4)


f = open("dict", "w", encoding="utf-8")
f.write(str(dictionary))
f.close()
