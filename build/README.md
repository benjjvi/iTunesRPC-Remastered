# Build Files

## AutoPyToExe

As you can see, the project is written in Python. To convert the program to an executeable file that can be run on Windows, I use auto-py-to-exe. These build files work with [auto-py-to-exe](https://pypi.org/project/auto-py-to-exe/). You will most likely need to modify paths to match those on your PC.


```config_album_artwork_creator.json``` = album artwork downloader

```config_windowed.json```              = windowed iTunesRPC-Remastered

```config_windowless.json```            = windowless iTunesRPC-Remastered

## InstallForge Files

To distribute the executeable files created by auto-py-to-exe, I use InstallForge to create a .exe file that allows for the program to be set up on the PC. The file is included, however there will probably be a lot of modifications that need to be made to make the script actually compile the software for you.