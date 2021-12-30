#LIBRARIES
import pypresence
import win32com.client
import time
import os

# TODO
# i) add error checking for if discord closes after it is opened
# ii) add playing/paused indicator in small_image

#VARIABLES
global_pause = 5 #set this higher if you get rate limited often by discord servers (reccomended: 5)
secret = open("secret", "r").readline() # discord client app secret
discord_path = open("discord_command", "r").readline() #this should be the command run to open discord
dict = eval(open("dict", "r", encoding="utf-8").read()) #the encoding is needed for other charsets e.g cyrillic

buttons = [
    {"label": "View on GitHub", "url": "https://github.com/bildsben/iTunesRPC-Remastered"}    
]

#DEFINITIONS
def push_playing(o, DiscordRPC, dict, last_pos, paused_track, moved_playhead):
    paused = False
    #Get all relevant information
    #TRACK INFO
    track = o.CurrentTrack.Name

    #OTHER INFO
    artist = o.CurrentTrack.Artist
    try:
        key_lookup = track + ":" + artist
        artwork_value = str(dict[key_lookup]) #artwork is directly uploaded to discord developer portal
    except Exception:
        print("This song has not had its artwork uploaded to the Discord Developer Portal.")
        print("Please upload it, then the blue question mark will be gone.")
        artwork_value = "error"

    #MODIFY TRACK TO HAVE PAUSED IF PAUSED ON APPLE MUSIC
    if paused_track:
        track = "[PAUSED] " + track

    #PRINT INFO
    print("Track: " + track)
    print("Artist: " + artist)
    print("Artwork Value: " + artwork_value)

    #timestamps for computing how far into the song we are
    if paused_track == False:
        starttime = int(time.time()) - o.PlayerPosition
        endtime = int(time.time()) + (o.CurrentTrack.Duration - o.PlayerPosition)

    if moved_playhead:
        DiscordRPC.clear() #get rid of the current status: the left count won't refresh otherwise.
        time.sleep(0.1) #if we don't pause for a tiny amount the .update will send, and discord will
        #forget the .clear command.

    if paused_track == True:
        if paused != True:
            DiscordRPC.update(details=track, state=artist, large_image=artwork_value, large_text=track, \
                              small_image="apple_music_icon", small_text="Playing on Apple Music", buttons=buttons)
            paused = True
    else:
        if last_pos != False:
            DiscordRPC.update(details=track, state=artist, start=starttime, end=endtime, large_image=artwork_value, large_text=track, \
                              small_image="apple_music_icon", small_text="Playing on Apple Music", buttons=buttons)
        else:
            last_pos = (o.CurrentTrack.Duration - o.PlayerPosition)
    
    
    return (track, artist, key_lookup, artwork_value, last_pos, paused)

#GETTING THE ITUNES COM CONNECTION
o = win32com.client.gencache.EnsureDispatch("iTunes.Application") #connect to the COM of iTunes.Application
print("Hooked to iTunes COM.")
# NOTE: win32com.client.gencache.EnsureDispatch will force open the application if not already open

#CONNECTING TO DISCORD
DiscordRPC = False
opened = False
while DiscordRPC == False:
    try:
        DiscordRPC = pypresence.Presence(secret, pipe=0)
        DiscordRPC.connect()
        print("Hooked to Discord.")
    except Exception:
        if not opened:
            os.system(discord_path)
            print("Attempting to open Discord.")
            opened = True
        time.sleep(global_pause+3) #takes a while to open discord on lower end hardware so account for that here
        continue

# GET LAST POSITION OF TRACK
stopped = True
while stopped:
    try:
        last_pos = (o.CurrentTrack.Duration - o.PlayerPosition)

        #LAST TRACK = THE TRACK THAT IS CURRENTLY PLAYED. IT MAKES SENSE IN 
        #CODE AS LAST_TRACK IS THE TRACK PLAYED {global_pause} SECONDS AGO
        last_track = o.CurrentTrack.Name
        track = o.CurrentTrack.Name
        stopped = False
    except Exception:
        DiscordRPC.clear()
        print(".........................................")
        print("    iTunes is not playing anything...    ")
        print(" Waiting for it to play before starting. ")
        print("            Waiting 3 seconds.           ")
        print(".........................................")
        time.sleep(3)

special_push = False # this is used to determine if another function has already pushed
# to RPC, as we don't want to repeat for loads of different items.

stopped = False
paused = False
first_run = True
while 1:
    if first_run:
        last_pos = (o.CurrentTrack.Duration - o.PlayerPosition)
        time.sleep(global_pause)
        first_run = False
    
    try:
        placeholder = o.CurrentTrack
    except Exception:
        stopped = True
    
    if stopped == False:
        print("------------------")

        # update the last track to be the variable that was playing 5 seconds ago and 
        # get the new current track and store it as track
        last_track = track
        track = o.CurrentTrack.Name

        print("Last Track: " + last_track)
        print("Current Track: " + track)

        print("Last Playhead Position: " + str(last_pos))
        print("Current Playhead Position: " + str((o.CurrentTrack.Duration - o.PlayerPosition)))
        print("Position Difference: " + str(last_pos - (o.CurrentTrack.Duration - o.PlayerPosition)))

        if last_track != track: # if we changed tracks.
            special_push = True
            print("Changed track. Getting regular fetch from push_playing.")
            track, artist, key_lookup, artwork_value, last_pos, paused = push_playing(o, DiscordRPC, dict, last_pos, False, False) 

        if not paused:
            if last_pos - (o.CurrentTrack.Duration - o.PlayerPosition) < global_pause-1 and last_pos - (o.CurrentTrack.Duration - o.PlayerPosition) >= 0:
                special_push = True
                # we are paused
                print("Paused. Sending pause message to RPC.")
                track, artist, key_lookup, artwork_value, last_pos, paused = push_playing(o, DiscordRPC, dict, last_pos, True, False)
            else:
                paused = False

            if (last_pos - (o.CurrentTrack.Duration - o.PlayerPosition) < 0 or last_pos - (o.CurrentTrack.Duration - o.PlayerPosition) > global_pause) and last_track == track:
                #we have rewound or fast forwarded within the song. let's make sure we account for that when calling push_playing
                #this could also happen when a new song has started. that is why last_track == track is in this if statement
                track, artist, key_lookup, artwork_value, last_pos, paused = push_playing(o, DiscordRPC, dict, last_pos, False, True)

            if special_push == False:
                track, artist, key_lookup, artwork_value, last_pos, paused = push_playing(o, DiscordRPC, dict, last_pos, False, False)
        
        special_push = False

        # get the last position of the track. used for pause
        last_pos = (o.CurrentTrack.Duration - o.PlayerPosition)
        time.sleep(global_pause)
    else:
        DiscordRPC.clear()
        print(".........................................")
        print("    iTunes is not playing anything...    ")
        print(" Waiting for it to play before starting. ")
        print("            Waiting 3 seconds.           ")
        print(".........................................")
        time.sleep(3)