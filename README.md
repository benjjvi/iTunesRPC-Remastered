# iTunesRPC-Remastered

A fork of [claythearc's iTunesRPC repo](https://github.com/claythearc/iTunesRPC) remastered to be a bit more feature rich.

Inspired by [nint8835's iTunesRichPresence repo](https://github.com/nint8835/iTunesRichPresence).

## IMPORTANT NOTE
To get the project to work, you must make an application in the [Discord Developer Portal](https://discord.com/developers/applications) and copy the
application ID into a file named ```secret```.
Additionally, you will need to have a file called ```discord_command``` with the command line command that can be used to execute discord from cmd. You can find this by right clicking your discord link on your desktop and copying the target text. 

Furthermore, to get the album artwork, please play your playlist in any order, on shuffle or in order, and play the script in the ```images``` folder named ```grabImages.py```. It will download the current playing album artwork, and after 5 seconds, get the current playing album artwork. To do this efficiently, have your finger on the ```FN``` key and press ```F8``` to skip songs. Once the command prompt says ```sleeping 5 seconds``` you can skip song. Please modify ```line 24``` in the file, as the counting will only stop after 33 songs (the length of my playlist), so please change this number to the length of your playlist (which can be found at the top, see below for an example).

![An image showing a cropped screenshot of an iTunes playlist named vibes 2.0, with a cover of a boy in a hoodie with the caption "roadman". Below the title of the playlist is the message "33 songs, totalling 1 hour and 37 minutes". Below this is a checkmark box that is ticked saying "publish on profile and in search".](/docs/1.png "My Playlist as an example.")

Original Features:
1. Shows currently playing song
2. Shows songs artist
3. Shows time left

New Features:
1. Paused message
2. Album Artwork (limited due to discord API)
3. Error Checking (is Discord open? If not, open it.)
4. Rewind Support (before, rewinding wouldn't modify anything with the client, but now it changes the time left variable.)