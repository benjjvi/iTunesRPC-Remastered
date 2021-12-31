#LIBRARIES
import pypresence
import win32com.client
import time
import os
from systray.traybar import SysTrayIcon

#VARIABLES
global_pause = 5 #set this higher if you get rate limited often by discord servers (reccomended: 5)
secret = open("secret", "r").readline() # discord client app secret
discord_path = open("discord_command", "r").readline() #this should be the command run to open discord
dict = eval(open("dict", "r", encoding="utf-8").read()) #the encoding is needed for other charsets 
                                                        #e.g cyrillic

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

    try:
        if moved_playhead:
            DiscordRPC.clear() #get rid of the current status: the left count won't refresh otherwise.
            time.sleep(0.1) #if we don't pause for a tiny amount the .update will send, and discord will
            #forget the .clear command.

        if paused_track == True:
            if paused != True:
                DiscordRPC.update(details=track, state=artist, large_image=artwork_value, large_text=track, \
                                small_image="apple_music_icon", small_text="Playing on Apple Music", \
                                buttons=buttons)
                paused = True
        else:
            if last_pos != False:
                DiscordRPC.update(details=track, state=artist, start=starttime, end=endtime, \
                                large_image=artwork_value, large_text=track, small_image="apple_music_icon", \
                                small_text="Playing on Apple Music", buttons=buttons)
            else:
                last_pos = (o.CurrentTrack.Duration - o.PlayerPosition)
        
    except Exception as e:
        #Discord is closed if we error here.
        #Let's re open it.
        print("..........................................")
        print(".           Discord is closed...         .")
        print(".          Attempting to open it         .")
        print(". Waiting global_pause+3 seconds before  .")
        print(".               continuing.              .")
        print("..........................................")

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
                    print("..........................................")
                    print(".           Discord is closed...         .")
                    print(".          Attempting to open it         .")
                    print(". Waiting global_pause+3 seconds before  .")
                    print(".               continuing.              .")
                    print("..........................................")
                    opened = True
                time.sleep(global_pause+3)
                continue

        #Now we have re opened Discord, let's post the message to Discord.

        time.sleep(global_pause)
        #Since we may have had Discord closed for a while, we need to update our items.
        #Let's re call this definition, as it ensures we get the most recent values.
        #We can send our original arguments to this. It isn't a massive deal.
        DiscordRPC, track, artist, key_lookup, artwork_value, last_pos, paused = push_playing(o, DiscordRPC, dict, last_pos, paused_track, moved_playhead)

    #Finally, regardless of what happened, let's return all our values.
    return (DiscordRPC, track, artist, key_lookup, artwork_value, last_pos, paused)

# Setting up systray
def exit_program(systray):
    global shutdown_systray
    shutdown_systray = True

menu_options = (("Shutdown iTunesRPC Safely", None, exit_program),)
systray = SysTrayIcon("icon.ico", "iTunesRPC", menu_options)
systray.start()
print("Started Systray icon.")

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
            print("..........................................")
            print(".           Discord is closed...         .")
            print(". Waiting for it to open before starting .")
            print(". Waiting global_pause+3 seconds before  .")
            print(".               continuing.              .")
            print("..........................................")
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
        print("..........................................")
        print(".    iTunes is not playing anything...   .")
        print(". Waiting for it to play before starting .")
        print(".           Waiting 3 seconds.           .")
        print("..........................................")
        time.sleep(3)

special_push = False # this is used to determine if another function has already pushed
# to RPC, as we don't want to repeat for loads of different items.

stopped = False
paused = False
first_run = True

shutdown_systray = False
running = True
while running:
    if first_run:
        last_pos = (o.CurrentTrack.Duration - o.PlayerPosition)
        time.sleep(global_pause)
        first_run = False
    
    try:
        placeholder = o.CurrentTrack.Name #try to get current track name
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
            DiscordRPC, track, artist, key_lookup, artwork_value, last_pos, paused = push_playing(o, DiscordRPC, dict, last_pos, False, False) 

        if not paused:
            if last_pos - (o.CurrentTrack.Duration - o.PlayerPosition) < global_pause-1 and last_pos - (o.CurrentTrack.Duration - o.PlayerPosition) >= 0:
                special_push = True
                # we are paused
                print("Paused. Sending pause message to RPC.")
                DiscordRPC, track, artist, key_lookup, artwork_value, last_pos, paused = push_playing(o, DiscordRPC, dict, last_pos, True, False)
            else:
                paused = False

            if (last_pos - (o.CurrentTrack.Duration - o.PlayerPosition) < 0 or last_pos - (o.CurrentTrack.Duration - o.PlayerPosition) > global_pause) and last_track == track:
                #we have rewound or fast forwarded within the song. let's make sure we account for that when calling push_playing
                #this could also happen when a new song has started. that is why last_track == track is in this if statement
                DiscordRPC, track, artist, key_lookup, artwork_value, last_pos, paused = push_playing(o, DiscordRPC, dict, last_pos, False, True)

            if special_push == False:
                DiscordRPC, track, artist, key_lookup, artwork_value, last_pos, paused = push_playing(o, DiscordRPC, dict, last_pos, False, False)
        
        special_push = False

        # get the last position of the track. used for pause
        last_pos = (o.CurrentTrack.Duration - o.PlayerPosition)
        time.sleep(global_pause)
    else:
        if stopped:
            DiscordRPC.clear()
            print("..........................................")
            print(".    iTunes is not playing anything...   .")
            print(". Waiting for it to play before starting .")
            print(".           Waiting 3 seconds.           .")
            print("..........................................")
            time.sleep(3)

    if shutdown_systray:
        running = False
        print("------------------")
        print("Shutting down.")

DiscordRPC.close()
print("Closed connection to DiscordRPC.")
systray.shutdown()
print("Shutdown the Systray icon.")
quit("Shutdown the Python program.")