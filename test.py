import pypresence
import win32com.client
import time

o = win32com.client.gencache.EnsureDispatch("iTunes.Application") #connect to the COM of iTunes.Application

secret = open("secret", "r").readline()

DiscordRPC = pypresence.Presence(secret, pipe=0)
DiscordRPC.connect()

#Get all relevant information
track = o.CurrentTrack.Name
artist = o.CurrentTrack.Artist
key_lookup = track + ":" + artist
artwork_value = str(dict[key_lookup]) #artwork is directly uploaded to discord developer portal

#timestamps for computing how far into the song we are
starttime = int(time.time()) - o.PlayerPosition
endtime = int(time.time()) + (o.CurrentTrack.Duration - o.PlayerPosition)

#ship it off
DiscordRPC.update(details=track, state=artist, start=starttime, end=endtime, large_image="1", large_text=track, small_image="2", small_text=track)



while True:
    time.sleep(5)