# encoding: utf-8
# iTuneRPC-Remastered
# github.com/bildsben/iTunesRPC-Remastered

# CORE LIBRARIES
import os
import platform  # for log info
import time
import psutil  # for log info
import sys  # exit at end of program: for compatibility with PyInstaller
import ast  # used for secure evaluation of strings from server; ty Neko#0013

# COM AND RPC LIBRARY
import win32com.client
import pypresence

# CUSTOM/MODIFIED LIBRARIES/MODULES
from module.itrpc_logging import log_message
from module.systray.traybar import SysTrayIcon
import module.connect_to_server as networking

# CONFIGURATION FILES
f = open("config", "r")
config = ast.literal_eval(f.read())  # returns dict
f.close()

# FIX FOR WINDOW
# this fix sets current song to not playing, artist to nothing and album to nothing.
curr = str({"song": "Not Playing", "artist": "", "album": ""})
x = open("current_song_info", "w")
x.write(curr)
x.close()

# CONSTS/VARS
domain = open("domain", "r").read()
global_pause = 5  # set this higher if you get rate limited often by discord servers (recomended: 5)

if config["slow_mode"] == True:
    global_pause += 5

try:
    import secret

    app_ID = secret.return_secret()
    del secret
    secret = app_ID
    del app_ID
except Exception:
    import module.itunesrpc_window.error_no_secret as ens  # error no secret (E.001.NS)

    ens.get_logger(log_message)
    ens.start()
    sys.exit()

try:
    discord_path = open(
        "discord_command", "r"
    ).readline()  # this should be the command run to open discord
except Exception as e:
    log_message("Error Occurred: " + e)
    discord_path = "C: && cd %appdata% && cd .. && cd Local\\Discord && Update.exe --processStart Discord.exe"

shutdown_systray = False
buttons = [
    {
        "label": "View on GitHub",
        "url": "https://github.com/bildsben/iTunesRPC-Remastered",
    }
]


# WINDOW
import module.itunesrpc_window.main as itrpc_window

itrpc_window.get_logger(log_message)  # send the logger instance
# main cannot access the logger otherwise.
itrpc_window.send_logger()
# this sends the logger to window_test

# the window can be opened by requesting the window in the system tray
# show brief message telling user about this.
if config["show_msg"] == True:
    itrpc_window.start_welcome()

# LOGGING
# first start: clean log messages and dump systeminfo
# none of this is automatically uploaded, but it should be
# sent within error reports on GitHub, as it may help determine
# your issue
os.remove("log")  # delete the old log file.
log_message("Starting system log dump.")
log_message("Machine Architecture: " + platform.machine())
log_message("Machine Version:" + platform.version())
log_message("Machine Platform: " + platform.platform())
log_message("Machine Unix Name: " + str(platform.uname()))
log_message("OS Type: " + platform.system())
log_message("Processor: " + platform.processor())
log_message(
    "Total RAM: " + str(round(psutil.virtual_memory().total / (1024.0**3))) + " GB"
)
log_message("End of system logs.\n")
log_message("Starting iTunesRPC logs.")


# DEFINITIONS
def push_playing(o, DiscordRPC, dict, last_pos, paused_track, moved_playhead):
    paused = False
    # Get all relevant information
    # TRACK INFO
    track = o.CurrentTrack.Name

    # OTHER INFO
    artist = o.CurrentTrack.Artist
    album = o.CurrentTrack.Album

    # SAVE DATA TO FILE, FOR WINDOW
    curr = str({"song": track, "artist": artist, "album": album})
    with open(
        "current_song_info", "w", encoding="utf-8"
    ) as current:  # save with context manager to allow for encoding= variable.
        current.write(curr)

    # MODIFY TRACK TO HAVE PAUSED IF PAUSED ON APPLE MUSIC
    if paused_track:
        track = "[PAUSED] " + track

    path = (os.path.dirname(os.path.realpath(__file__))) + rf"\\" + str("temp") + ".png"

    if path[:2] == r"\\":
        exit("You are running on a network server.\nPlease use a local folder.")

    o.CurrentTrack.Artwork.Item(1).SaveArtworkToFile(path)

    artwork_url = networking.get("temp.png", domain, track, artist, album)
    print(artwork_url)
    print(str(artwork_url))
    artwork_url = ast.literal_eval(str(artwork_url))

    artwork_url = str(artwork_url[1]) + str(artwork_url[2])
    artwork_url = "https://" + domain + "/itrpc/" + artwork_url

    os.remove("temp.png")

    # log_message INFO
    log_message("Track: " + track)
    log_message("Artist: " + artist)
    log_message("Album: " + album)
    log_message("Artwork URL: " + str(artwork_url))

    pause_button = f"https://{domain}/itrpc/pause.png"
    play_button = f"https://{domain}/itrpc/play.png"

    # timestamps for computing how far into the song we are
    if paused_track == False:
        starttime = int(time.time()) - o.PlayerPosition
        endtime = int(time.time()) + (o.CurrentTrack.Duration - o.PlayerPosition)

    try:
        if moved_playhead:
            DiscordRPC.clear()  # get rid of the current status: the left count won't refresh otherwise.
            time.sleep(0.1)
            # if we don't pause for a tiny amount the .update will send, and discord will
            # forget the .clear command.

        if paused_track == True:
            if paused != True:
                DiscordRPC.update(
                    details=track,
                    state=artist,
                    large_image=artwork_url,
                    large_text=album,
                    small_image=pause_button,
                    small_text="Paused on Apple Music",
                    buttons=buttons,
                )
                paused = True
        else:
            if last_pos != False:
                DiscordRPC.update(
                    details=track,
                    state=artist,
                    start=starttime,
                    end=endtime,
                    large_image=artwork_url,
                    large_text=album,
                    small_image=play_button,
                    small_text="Playing on Apple Music",
                    buttons=buttons,
                )
            else:
                last_pos = o.CurrentTrack.Duration - o.PlayerPosition

    except Exception as e:
        # Discord is closed if we error here.
        # Let's re open it.
        log_message("..........................................")
        log_message(".           Discord is closed...         .")
        log_message(".          Attempting to open it         .")
        log_message(". Waiting global_pause+3 seconds before  .")
        log_message(".               continuing.              .")
        log_message("..........................................")

        DiscordRPC = False
        opened = False

        while DiscordRPC == False:
            try:
                DiscordRPC = pypresence.Presence(secret, pipe=0)
                DiscordRPC.connect()
                log_message("Hooked to Discord.")
            except Exception:
                if not opened:
                    os.system(discord_path)
                    log_message("..........................................")
                    log_message(".           Discord is closed...         .")
                    log_message(".          Attempting to open it         .")
                    log_message(". Waiting global_pause+3 seconds before  .")
                    log_message(".               continuing.              .")
                    log_message("..........................................")
                    opened = True
                time.sleep(global_pause + 3)
                continue

        # Now we have re opened Discord, let's post the message to Discord.

        time.sleep(global_pause)
        # Since we may have had Discord closed for a while, we need to update our items.
        # Let's re call this definition, as it ensures we get the most recent values.
        # We can send our original arguments to this. It isn't a massive deal.
        DiscordRPC, track, artist, album, last_pos, paused = push_playing(
            o, DiscordRPC, dict, last_pos, paused_track, moved_playhead
        )

    # Finally, regardless of what happened, let's return all our values.
    return (DiscordRPC, track, artist, album, last_pos, paused)


# SYSTRAY DEFINITIONS
# window definitions defined at start of program.
def exit_program(systray):
    global shutdown_systray
    shutdown_systray = True


def toggle_rpc(systray):
    global toggled
    toggled = not toggled
    time.sleep(global_pause + 1)
    DiscordRPC.clear()


# SYSTRAY MENU OPTIONS AND MAKING THE ICON
menu_options = (
    ("Show Window", None, itrpc_window.start),
    ("Toggle Rich Presence", None, toggle_rpc),
    ("Shutdown iTunesRPC Safely", None, exit_program),
)
systray = SysTrayIcon("icon.ico", "iTunesRPC", menu_options)
systray.start()
log_message("Started Systray icon.")


# GETTING THE ITUNES COM CONNECTION
o = win32com.client.gencache.EnsureDispatch(
    "iTunes.Application"
)  # connect to the COM of iTunes.Application
log_message("Hooked to iTunes COM.")
# NOTE: win32com.client.gencache.EnsureDispatch will force open the application if not already open


# CONNECTING TO DISCORD
DiscordRPC = False
opened = False
while DiscordRPC == False:
    if shutdown_systray:
        log_message("No connection to DiscordRPC, so not closing.")
        systray.shutdown()
        log_message("Shutdown the Systray icon.")
        quit("Shutdown the Python program.")
    try:
        DiscordRPC = pypresence.Presence(secret, pipe=0)
        DiscordRPC.connect()
        log_message("Hooked to Discord.")
    except Exception:
        if not opened:
            os.system(discord_path)
            log_message("..........................................")
            log_message(".           Discord is closed...         .")
            log_message(". Waiting for it to open before starting .")
            log_message(". Waiting global_pause+3 seconds before  .")
            log_message(".               continuing.              .")
            log_message("..........................................")
            opened = True
        time.sleep(
            global_pause + 3
        )  # takes a while to open discord on lower end hardware so account for that here
        continue


# GET LAST POSITION OF TRACK
stopped = True
while stopped:
    try:
        last_pos = o.CurrentTrack.Duration - o.PlayerPosition
        # LAST TRACK = THE TRACK THAT IS CURRENTLY PLAYED. IT MAKES SENSE IN
        # CODE AS LAST_TRACK IS THE TRACK PLAYED {global_pause} SECONDS AGO
        last_track = o.CurrentTrack.Name
        track = o.CurrentTrack.Name
        stopped = False
    except Exception:
        DiscordRPC.clear()
        o = win32com.client.gencache.EnsureDispatch("iTunes.Application")
        log_message("..........................................")
        log_message(".    iTunes is not playing anything...   .")
        log_message(". Waiting for it to play before starting .")
        log_message(".           Waiting 10 seconds.          .")
        log_message("..........................................")
        time.sleep(10)


# LOOP VARIABLES
special_push = False  # this is used to determine if another function has already pushed
# to RPC, as we don't want to repeat for loads of different items.

stopped = False  # track stopped (iTunes has no track selected)
paused = False  # track paused (iTunes has a track selected)
first_run = True  # first ran the program.
shutdown_systray = False  # shutdown the program from the systray
running = True  # run var
skipped = False  # skipping song.
toggled = True  # showing RP?


# LOOP
while running:
    if toggled:
        if first_run:
            last_pos = o.CurrentTrack.Duration - o.PlayerPosition
            time.sleep(global_pause)
            first_run = False

        try:
            placeholder = o.CurrentTrack.Name  # try to get current track name
        except Exception:
            stopped = True

        if stopped == False:
            log_message("------------------")

            # update the last track to be the variable that was playing 5 seconds ago and
            # get the new current track and store it as track
            last_track = track
            track = o.CurrentTrack.Name

            log_message("Last Track: " + last_track)
            log_message("Current Track: " + track)

            log_message("Last Playhead Position: " + str(last_pos))
            log_message(
                "Current Playhead Position: "
                + str((o.CurrentTrack.Duration - o.PlayerPosition))
            )
            log_message(
                "Position Difference: "
                + str(last_pos - (o.CurrentTrack.Duration - o.PlayerPosition))
            )
            log_message("Pushing the following info...")

            if last_track != track:  # if we changed tracks.
                special_push = True
                skipped = True
                log_message("Changed track. Getting regular fetch from push_playing.")
                DiscordRPC, track, artist, album, last_pos, paused = push_playing(
                    o, DiscordRPC, dict, last_pos, False, False
                )

            if not paused or not skipped:
                if (
                    last_pos - (o.CurrentTrack.Duration - o.PlayerPosition)
                    < global_pause - 1
                    and last_pos - (o.CurrentTrack.Duration - o.PlayerPosition) >= 0
                ):
                    special_push = True
                    # we are paused
                    log_message("Paused. Sending pause message to RPC.")
                    DiscordRPC, track, artist, album, last_pos, paused = push_playing(
                        o, DiscordRPC, dict, last_pos, True, False
                    )
                else:
                    paused = False

                if (
                    (last_pos - (o.CurrentTrack.Duration - o.PlayerPosition) < 0)
                    or (
                        last_pos - (o.CurrentTrack.Duration - o.PlayerPosition)
                        > global_pause + 1
                    )
                ) and last_track == track:
                    # we have rewound or fast forwarded within the song. let's make sure we account for that when calling push_playing
                    # this could also happen when a new song has started. that is why last_track == track is in this if statement
                    log_message(
                        "Track position moved over global_pause value, likely skipped forward/backward in the song."
                    )
                    special_push = True
                    DiscordRPC, track, artist, album, last_pos, paused = push_playing(
                        o, DiscordRPC, dict, last_pos, False, True
                    )

                if special_push == False:
                    DiscordRPC, track, artist, album, last_pos, paused = push_playing(
                        o, DiscordRPC, dict, last_pos, False, False
                    )
            else:
                skipped = False

            special_push = False

            # get the last position of the track. used for pause
            last_pos = o.CurrentTrack.Duration - o.PlayerPosition
            time.sleep(global_pause)
        else:
            DiscordRPC.clear()
            try:
                del o
            except Exception:
                pass
            o = win32com.client.gencache.EnsureDispatch("iTunes.Application")
            log_message("..........................................")
            log_message(".    iTunes is not playing anything...   .")
            log_message(". Waiting for it to play before starting .")
            log_message(".           Waiting 10 seconds.          .")
            log_message("..........................................")
            time.sleep(10)

            stopped = False
            try:
                track = o.CurrentTrack.Name
            except Exception as e:
                log_message(e)
                stopped = True

        if shutdown_systray:
            running = False
            log_message("------------------")
            log_message("Shutting down.")
    else:
        log_message("RPC is toggled off. Not showing status.")
        log_message("Waiting 1 second to check if toggled is enabled.")
        time.sleep(1)


# SHUTDOWN
DiscordRPC.close()
log_message("Closed connection to DiscordRPC.")

systray.shutdown()
log_message("Shutdown the Systray icon.")

o.Quit()
log_message("Closed iTunes connection.")

p = open("config", "r")
prev = ast.literal_eval(p.readline())
p.close()
prev["gui_window_isOpen"] = False
update = open("config", "w")
update.write(str(prev))
update.close()
log_message(
    "Set GUI isOpen to False to ensure we don't get hanging on next open."
)  # If this value is left as true, on the next launch of the app, it is possible that the window will freeze.

sys.exit(log_message("Shutdown application."))
