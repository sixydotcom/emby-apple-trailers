"""
Prerequisites:
    python3
    feedparser and youtube-dl packages (pip3 install feedparser youtube-dl)

Usage: 
    Change the trailers_library path
    Change the rssurl and/or preferred_resolution if desired.
    Run the script
"""

import feedparser, os
from youtube_dl import YoutubeDL

#************************************************************************************************************************
rssurl               = "https://trailers.apple.com/trailers/home/rss/newtrailers.rss"  #url of the apple trailer rss feed
preferred_resolution = "hd1080"         #preferred resolution of the trailer - valid options are "sd" "hd720" or "hd1080"   
trailers_library     = "./Trailers/"     #base path for Trailers library
#************************************************************************************************************************
  

#use feedparser to grab rss feed and extract all trailer titles and urls
#returns a dictionary - format is {'Movie name': ['http://trailers.apple.com/trailer1.mov','http://trailers.apple.com/trailer2.mov']}
def get_feed(url):
    feed = feedparser.parse(rssurl)

    #create dictionary with movie name and list of trailer direct urls
    dict = {}
    for entry in feed['entries']:
        try:
            entry_title = entry['title'].split(" - ")[0]    
        except:
            entry_title = entry['title']
        trailers = get_video_url(entry['link'], preferred_resolution)
        if len(trailers) > 0:
            dict[entry_title] = trailers
    return dict

#use youtube-dl to find the direct urls of trailer video files
def get_video_url(url, res):
    direct_urls = []
    with YoutubeDL() as ydl:
        info_dict = ydl.extract_info(url, download=False)

    for entry in info_dict['entries']:      
        for f in entry['formats']:
            if f['format_id'].endswith(res):
                fname = os.path.basename(f['url'])
                if ("trailer" in fname or "teaser" in fname): #only get teasers and trailers. ignore clips
                    direct_urls.append(f['url'])
    return direct_urls
    
#function to normalize the name of the movie to remove invalid chars for file names
def normalize_filename(str):
    bad_chars = '<>:"/\|?*'
    for char in bad_chars:
        str = str.replace(char, '')
    return str

#create directories and write out strm files if they don't exist
def write_strm_files(trailer_dict):
    for movie in trailer_dict:
        for trailer in trailer_dict[movie]:
            trailer_basename = os.path.splitext(os.path.basename(trailer))[0] #get the direct trailer filename without an extension so we can add a .strm to the end
            
            movie_path = os.path.join(trailers_library, normalize_filename(movie))   #output example c:\Emby\Trailers\Movie
            trailer_path = os.path.join(movie_path, "trailers")                      #output example c:\Emby\Trailers\Movie\trailers 
            movie_strm = os.path.join(movie_path, normalize_filename(movie) + ".strm")
            trailer_strm = os.path.join(trailer_path, trailer_basename + ".strm")

            if not os.path.exists(trailers_library):
                os.mkdir(trailers_library)                
            if not os.path.exists(movie_path):
                os.mkdir(movie_path)
            if not os.path.exists(trailer_path):
                os.mkdir(trailer_path)
            if not os.path.exists(movie_strm):
                f = open(movie_strm, "w")
                f.write(trailer)
                f.close()                
            if not os.path.exists(trailer_strm):
                print(f"New trailer found for {movie}")
                f = open(trailer_strm, "w")
                f.write(trailer)
                f.close()                    


#build the trailer dictionary
trailer_dict = get_feed(rssurl)

#create dirs and write out strm files
write_strm_files(trailer_dict)


