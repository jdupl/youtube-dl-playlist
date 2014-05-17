youtube-dl-playlist

Author: Jordon Mears <jordoncm at gmail dot com>
Fork author: Justin Duplessis <duplessisjustin1 at gmail dot com>
License: LGPL version 2 or greater <http://www.gnu.org/licenses/lgpl.html>

Usage: youtube-dl-playlist PLAYLIST_ID [DESTINATION_PATH]

This utility allows you to download all the videos from a playlist on Youtube. 
It creates a folder in the current directory (or in the specified path) named 
after the playlist name and then downloads each video in order and places it 
within the folder.

If the script fails in the middle of the playlist you can restart it with the 
same options and should pick up where it left off.

Forked for Python 3 and keep playlist order in video filenames.

Depends on:
 - Python 3 (should be available on Linux/Unix/Mac by default)
 - youtube-dl (avaliable at http://rg3.github.com/youtube-dl/ and in repos for 
   most Linux distros)

To install:
Install [youtube-dl-playlist](https://github.com/jordoncm/youtube-dl-playlist)

Download the python file and save to /usr/local/bin/youtube-dl-channel

`sudo curl https://raw.githubusercontent.com/jdupl/youtube-dl-channel/master/youtube-dl-playlist.py -o /usr/local/bin/youtube-dl-playlist`

Give execute rights

`sudo chmod a+x /usr/local/bin/youtube-dl-playlist`
