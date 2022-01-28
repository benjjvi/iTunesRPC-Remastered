# iTunesRPC-Remastered
Discord Rich Presence for iTunes on Windows.

![The application in use.](/docs/a.png)

[![pypresence](https://img.shields.io/badge/using-pypresence-00bb88.svg?style=for-the-badge&logo=discord&logoWidth=20)](https://github.com/qwertyquerty/pypresence)

A fork of [claythearc's iTunesRPC repo](https://github.com/claythearc/iTunesRPC) remastered to be a bit more feature rich.

Inspired by [nint8835's iTunesRichPresence repo](https://github.com/nint8835/iTunesRichPresence).

Using minimally modified code from [Infinidat's infi.systray module](https://github.com/Infinidat/infi.systray). This repo therefore uses their [BSD 3-Clause 'New' or 'Revised' License](https://github.com/Infinidat/infi.systray/blob/develop/LICENSE) 
provided within their GitHub repo.

Current Line Count: ```1,362 (Last count @ 23:01, 28 Jan 2022)```

## LICENSES

This repository contains code from INFIDAT with their infi.systray code. Their license for the code can be found [here](/LICENSES/INFIDAT-License). This repository also contains code from qwertyqwerty with their pypresence library. Their license for the code can be found [here](/LICENSES/pypresence-License). Additionally, the repository is licenses under its own ```Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)``` License. The simplified version can be found [here](/LICENSES/Simplified-iTunesRPC-License), and the full version can be found [here](/LICENSES/Full-iTunesRPC-License). In the case of a legal dispute, the one applicable by law to the code provided in this software is the [full license](/LICENSES/Full-iTunesRPC-License). 

## TROUBLESHOOTING

If you get an error message when the application tries to launch Discord, you may need to change the file named discord_command, even if you downloaded the .ZIP file containing the files .EXE format.

## SELF HOSTING THE SERVER

Want to host the server yourself? Go for it! Place the server.py, all_files, and run.sh files into a folder that can be accessed externally on a HTTPS connection. Run the run.sh file, and the web server will start itself up. When running itunesrpc.py, edit the domain file to have your web servers domain instead of the default.

## IMPORTANT NOTE
Since the last update of this program, the album artwork automatically uploads to a server for you as discord has allowed rich presence images to contact outside servers! The server is defined in the ```domain``` file, and should NOT have a http(s)://or a trailing / at the end of the url. Additionally, the file server that the artwork is uploaded to should be available at ```https://your_url.com/itrpc/server.py```. If this returns an error, you have not set up the server correctly, as the server.py file, and the all_files file should be accessible on the internet as that is the folder that the images get saved to. The files in the "static" folder should also be placed in that folder with the same name that they have at the moment. However, what hasn't changed since the last update is the need for an AppID to be found in the home folder of the project. An AppID is not required to be added for the compiled executeable, as it is bundled with the EXE, however it is necessary if you plan on runing the raw python files.

The file should be named secret.py, and contain the following line.
```def return_secret() -> int: return int(your_app_id)```

## Features
Original Features:
1. Shows currently playing song
2. Shows songs artist
3. Shows time left

New Features:
1. Paused message
2. Album Artwork
3. Error Checking (is Discord open? If not, open it. Is iTunes playing anything? if not, clear rich presence)
4. Rewind Support (before, rewinding wouldn't modify anything with the client, but now it changes the time left variable.)
