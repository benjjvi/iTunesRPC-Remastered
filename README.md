# iTunesRPC-Remastered

A fork of [claythearc's iTunesRPC repo](https://github.com/claythearc/iTunesRPC) remastered to be a bit more feature rich.

Inspired by [nint8835's iTunesRichPresence repo](https://github.com/nint8835/iTunesRichPresence).

## IMPORTANT NOTE
To get the project to work, you must make an application in the [Discord Developer Portal](https://discord.com/developers/applications) and copy the
application ID into a file named ```secret```.
Additionally, you will need to have a file called ```discord_command``` with the command line command that can be used to execute discord from cmd. You can find this by right clicking your discord link on your desktop and copying the target text.

Original Features:
1. Shows currently playing song
2. Shows songs artist
3. Shows time left

New Features:
1. Paused message
2. Album Artwork (limited due to discord API)
3. Error Checking (is Discord open? If not, open it.)