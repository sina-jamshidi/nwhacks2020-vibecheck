# Scrape text and annotations for themes/mood
# Match the themes/moods with user inputted text

import requests
import pprint
import lyricsgenius

class GeniusManager:
    accessToken = None

    def __init__(self):
        self.accessToken = "USa7ebv_3Dn8NR-H6KQ14MQcGPinChBi9E8F-HMQyFCW-wLVP2aPoD40oRKJSd7g"

    #Input: List of [Dictonaries of Tracks]
    #Output: Return List of Dictionaries (now with Lyrics)
    def getLyrics(self, songlst):
        genius = lyricsgenius.Genius(self.accessToken)
        genius.remove_section_headers = True
        for i in range(len(songlst)):
            songTitle = songlst[i]["name"]
            songArtist = songlst[i]["artist"]

            if "(with" in songTitle:
                songTitle = songTitle.split("(")[0].strip()

            
            geniusSong = genius.search_song(songTitle,artist=songArtist, get_full_info=False)
            songlst[i]['lyrics'] = geniusSong.lyrics.replace("\n"," ")
            if songArtist.lower() not in geniusSong.artist.lower():
                songlst[i]['lyrics'] = None
        
        return songlst
