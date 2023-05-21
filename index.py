# FOR SCRAPING FROM YOUTUBE
import selenium
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
#For Downloading from youtube
from pytube import YouTube
# import youtube_dl
from pathlib import Path
import time
import os
#FOR SPOTIFY
import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="36827dd3128c4d9390b68d7011c54a8a",
                                               client_secret="747e4ae2f1b34412830b94f68b0d04bf",
                                               redirect_uri="http://localhost:8888/callback",
                                               scope="user-library-read"))

#Fetching Songs data from spotify
# results = sp.current_user_saved_tracks(limit=50)
songs=[]
# for idx, item in enumerate(results['items']):
#     track = item['track']
#     song=track['name']+" "+track['artists'][0]['name']
#     songs.append(song)

# for idx, item in enumerate(songs):
#     print(item)

# Get a playlist 
playlist_link = "https://open.spotify.com/playlist/37i9dQZF1DXbQDZkQM83q7?si=72e2cb1275874ecd"
playlist_URI = playlist_link.split("/")[-1].split("?")[0]
track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]
for item in sp.playlist_tracks(playlist_URI)["items"]:
    #Track name
    track = item['track']
    song=track['name']+" "+track['artists'][0]['name']
    print(song)
    songs.append(song)

# Searching for songs on youtube and downloading them - using selenium
options = Options()
options.headless = True
browser = webdriver.Chrome(options=options)
browser.get('https://youtube.com/')
wait = WebDriverWait(browser, 3)
presence = EC.presence_of_element_located
visible = EC.visibility_of_element_located
urls=[]
# Extracting songs from youtube
for idx, item in enumerate(songs):
    song=item
    browser.get("https://www.youtube.com/results?search_query=" + str(song))
    time.sleep(1)
    video=browser.find_element('xpath','//*[@id="video-title"]').get_attribute('href')
    print(video)
    urls.append(video)

    destination = "/home/abhinav/Downloads"
    
    # link of the video to be downloaded 
    link=video
    yt=YouTube(link,use_oauth=True, allow_oauth_cache=True)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=destination)
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    print(yt.title + " has been successfully downloaded.")
        
    
# download_ytvid_as_mp3()

# playlists = sp.current_user_playlists()
# while playlists:
#     for i, playlist in enumerate(playlists['items']):
#         print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
#     if playlists['next']:
#         playlists = sp.next(playlists)
#     else:
#         playlists = None

# FOR DOWNLOADING UING YOUTUBE_DL
        # try: 
        #     # object creation using YouTube
        #     # which was imported in the beginning 
        #     yt = YouTube(str(link))
        #     audio = yt.streams.filter(only_audio=True).first() 
        # except: 
        #     print("Connection Error") #to handle exception 
  
        # # filters out all the files with "mp4" extension 
        # base, ext = os.path.splitext(SAVE_PATH)
        # new_file=base + '.mp3'
        # os.rename(SAVE_PATH, new_file)

        # print(yt.title+"Successfully downloaded")