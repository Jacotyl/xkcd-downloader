# xkcd-downloader
A script to download images from the webcomic site https://xkcd.com/, which also shows off both sequential and async download methods and the speed increase from using async.

This program will create 2 folders in the directory the program is launched from: xkcd_serial and xkcd_async.
In my testing, Async has a 4-5x speed increase over serial. I have only tested with ~100 images though.

You can edit lowerBound and upperBound to change the range of images downloaded.
