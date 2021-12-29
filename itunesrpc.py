import pypresence
import win32com.client
import time
import os

secret = open("secret", "r").readline() # discord client app secret

discord_path = open("discord_command", "r").readline() #this should be the command run to open discord

dict = eval(open("dict", "r").read())

def push_playing(o, DiscordRPC, dict):
    #Get all relevant information
    track = o.CurrentTrack.Name
    artist = o.CurrentTrack.Artist
    key_lookup = track + ":" + artist
    artwork_value = str(dict[key_lookup]) #artwork is directly uploaded to discord developer portal

    #timestamps for computing how far into the song we are
    starttime = int(time.time()) - o.PlayerPosition
    endtime = int(time.time()) + (o.CurrentTrack.Duration - o.PlayerPosition)

    DiscordRPC.update(details=track, state=artist, start=starttime, end=endtime, large_image=artwork_value, large_text=track, small_image="apple_music_icon", small_text="Playing on Apple Music")
    return (track, artist, key_lookup, artwork_value)

o = win32com.client.gencache.EnsureDispatch("iTunes.Application") #connect to the COM of iTunes.Application
# NOTE: win32com.client.gencache.EnsureDispatch will force open the application if not already open

DiscordRPC = False
while DiscordRPC == False:
    try:
        DiscordRPC = pypresence.Presence(secret, pipe=0)
        DiscordRPC.connect()
    except Exception:
        os.system(discord_path)
        print("PLEASE OPEN DISCORD")
        time.sleep(5)
        continue

if o.CurrentTrack != None:
    track, artist, key_lookup, artwork_value = push_playing(o, DiscordRPC, dict)
else:
    last_pos = 0

paused = False
new_play = False #only just started playing music

while True:
    time.sleep(5)
    if o.CurrentTrack != None:
        if new_play == True:
            new_play = False 
            track, artist, key_lookup, artwork_value = push_playing(o, DiscordRPC, dict)

            last_pos = (o.CurrentTrack.Duration - o.PlayerPosition)
        else:
            if track == o.CurrentTrack.Name:
                print((o.CurrentTrack.Duration - o.PlayerPosition))
                print(last_pos)
                if not paused:
                    if last_pos - (o.CurrentTrack.Duration - o.PlayerPosition) < 3 or (o.CurrentTrack.Duration - o.PlayerPosition) - last_pos == 0:
                        #assume player is paused
                        paused = True
                        new_track = "[PAUSED] " + track
                        DiscordRPC.update(state=artist, details=new_track, large_image=artwork_value, large_text=new_track, small_image="apple_music_icon", small_text="Playing on Apple Music")
                else:
                    print(last_pos - (o.CurrentTrack.Duration - o.PlayerPosition))
                    if last_pos - (o.CurrentTrack.Duration - o.PlayerPosition) > 3:
                        print("UPDATING")
                        paused = False
                        track, artist, key_lookup, artwork_value = push_playing(o, DiscordRPC, dict)
                last_pos = (o.CurrentTrack.Duration - o.PlayerPosition)

            else:
                track, artist, key_lookup, artwork_value = push_playing(o, DiscordRPC, dict)
    else:
        DiscordRPC.clear()
        new_play = True