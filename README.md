# emby-apple-trailers.py

The purpose of this script is to build a local movie trailers library for Emby using the Apple Trailers RSS feed. Using the RSS feed and youtube-dl it builds strm files containing the link to the direct video. 


## Prerequisites

[Python3](https://www.python.org/downloads/)

After installing python, install the following packages:
[feedparser](https://pypi.org/project/feedparser/) - pip3 install feedparser
[youtube_dl](https://pypi.org/project/youtube_dl/) - pip3 install youtube_dl

## Downloading & configuring

Download the latest version from the [releases](https://github.com/lozengenods/emby-apple-trailers/releases)
Extract the files to your preferred location.
Edit emby-apple-trailers.py with your favorite text editor
Change the trailers_library setting to your output preference, for example:
- "/home/lozengenods/Emby/Trailers/" 
- "c:/users/lozengenods/Emby/Trailers/"

## Running

Windows: py emby-apple-trailers.py
Linux: python3 emby-apple-trailers.py

## Scheduling Examples

Ubuntu Linux using cron:

From bash prompt: crontab -e
Add this line to run once a day at 8pm: 0 20 * * * python3 /home/lozengenods/Emby/scripts/emby-apple-trailers.py
Save (CTRL+O) & exit (CTRL+X)

