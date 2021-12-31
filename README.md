# iTunesRPC-Remastered
Discord Rich Presence for iTunes on Windows.

![The application in use.](/docs/a.png)

[![pypresence](https://img.shields.io/badge/using-pypresence-00bb88.svg?style=for-the-badge&logo=discord&logoWidth=20)](https://github.com/qwertyquerty/pypresence)

A fork of [claythearc's iTunesRPC repo](https://github.com/claythearc/iTunesRPC) remastered to be a bit more feature rich.

Inspired by [nint8835's iTunesRichPresence repo](https://github.com/nint8835/iTunesRichPresence).

Using minimally modified code from [Infinidat's infi.systray module](https://github.com/Infinidat/infi.systray). This repo therefore uses their [BSD 3-Clause 'New' or 'Revised' License](https://github.com/Infinidat/infi.systray/blob/develop/LICENSE) 
provided within their GitHub repo.

## LICENSES

This repository contains code from INFIDAT with their infi.systray code. Their license for the code can be found [here](/LICENSES/INFIDAT-License). This repository also contains code from qwertyqwerty with their pypresence library. Their license for the code can be found [here](/LICENSES/pypresence-License). Additionally, the repository is licenses under its own ```Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)``` License. The simplified version can be found [here](/LICENSES/Simplified-iTunesRPC-License), and the full version can be found [here](/LICENSES/Full-iTunesRPC-License). In the case of a legal dispute, the one applicable by law to the code provided in this software is the [full license](/LICENSES/Full-iTunesRPC-License). 

## TROUBLESHOOTING

If you get an error message when the application tries to launch Discord, you may need to change the file named discord_command, even if you downloaded the .ZIP file containing the files .EXE format.

## IMPORTANT NOTE
To get the project to work, you must make an application in the [Discord Developer Portal](https://discord.com/developers/applications) and copy the
application ID into a file named ```secret```. You will need to upload all of the images in the ```static``` folder to your Discord Developer Portal application.
Additionally, you will need to have a file called ```discord_command``` with the command line command that can be used to execute discord from cmd. You can find this by right clicking your discord link on your desktop and copying the target text. 

Furthermore, to get the album artwork, please play your playlist, be it on shuffle or in order, and run the script in the ```images``` folder named ```grabImages.py```. It will download the current playing album artwork, and after 5 seconds, get the current playing album artwork. To do this efficiently, have your finger on the ```FN``` key and press ```F8``` (or whichever key is your keyboards skip song key) to skip songs. Once the command prompt says ```sleeping 5 seconds``` you can skip song. When starting the script, you'll be asked to provide a starting and ending number. If this is the first time running the script, type 1 as the starting number, and the length of your playlist as the ending number. For example, to add the playlist below, I would submit 1 as the starting number and 33 as the final number.

![An image showing a cropped screenshot of an iTunes playlist named vibes 2.0, with a cover of a boy in a hoodie with the caption "roadman". Below the title of the playlist is the message "33 songs, totalling 1 hour and 37 minutes". Below this is a checkmark box that is ticked saying "publish on profile and in search".](/docs/1.png "My Playlist as an example.")

If this is not your first time adding to the library of artwork, you should set the start number to one above the highest you have at the moment. For example, the playlist above has 33 songs, I would set the starting number as 34 to add a new playlist's artwork. When you have all the images you would like, first, move the ```dict``` file that was created in the ```images``` folder to the folder above (the one containing the itunesrpc.py script). After you have copied the ```dict``` file, you will need to upload the artwork images to your discord application thorugh the [Discord Developer Portal](https://discord.com/developers/applications).

1. Head over to the [Discord Developer Portal](https://discord.com/developers/applications) and select your application. Mine is called Apple Music, as you can see in [this image](/docs/2.png).
2. Select the application by clicking its icon, then press the Rich Presence option on the left hand menu. It should look like [this](/docs/3.png)
3. Press the [Rich Presence > Art Assets](/docs/4.png) option.
4. Select [add images](/docs/5.png) and add all your images WITHOUT changing the file names. The ```dict``` file holds a copy of each song with the number that corresponds with that song.

## Features
Original Features:
1. Shows currently playing song
2. Shows songs artist
3. Shows time left

New Features:
1. Paused message
2. Album Artwork (limited due to discord API)
3. Error Checking (is Discord open? If not, open it. Is iTunes playing anything? if not, clear rich presence)
4. Rewind Support (before, rewinding wouldn't modify anything with the client, but now it changes the time left variable.)

## Limitations
1. Album Artwork has to be manually uploaded, and can only hold up to 296 images at a time (-4 for error, apple music icon, play icon and pause icon).