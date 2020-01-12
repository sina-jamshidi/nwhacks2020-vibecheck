import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

# Jordan's Spotify ID: 12160864262
# You need to use your own Spotify ID if you want to log in to your account

# Client ID: ee266f2e282940178c0db7214c9822ce
# Client Secret: f76d68e6152a44dab93b9a745e638ff3
# Redirect URI: http://google.com/

# You also need to set ENVIRONMENT VARIABLES in your terminal:
# export SPOTIPY_CLIENT_ID='ee266f2e282940178c0db7214c9822ce'
# export SPOTIPY_CLIENT_SECRET='f76d68e6152a44dab93b9a745e638ff3'
# export SPOTIPY_REDIRECT_URI='http://google.com/'

class SpotifyManager:

    def __init__(self, username):
        self.username = username
        scope = 'user-top-read'
        # Erase cache, prompt for user permission, and specify scope(s) to use
        try:
            token = util.prompt_for_user_token(self.username, scope)
        except:
            os.remove(f".cache-{self.username}")
            token = util.prompt_for_user_token(self.username, scope)
        # Create our spotifyObject
        self.spotifyObject = spotipy.Spotify(auth=token)

    # Return a list of URI for user's top tracks
    def getTopTracks(self, limit=20):
        result = []
        topTracks = self.spotifyObject.current_user_top_tracks(limit=limit)
        for item in topTracks['items']:
            result.append(item['uri'])
        return result

    # Return audio features for one/multiple tracks
    def getAudioFeatures(self, tracks):
        audioFeatures = self.spotifyObject.audio_features(tracks)
        return audioFeatures

    # Return a list of recommended tracks for one to five seeds
    def getRecommendations(self, tracks, limit=10):
        songData = {}
        result = []
        recommendationTracks = self.spotifyObject.recommendations(seed_tracks=tracks, limit=limit)
        for track in recommendationTracks['tracks']:
            songData['name'] = track['name']
            songData['artist'] = track['artists'][0]['name']
            songData['uri'] = track['uri']
            songData['albumPic'] = track['album']['images'][0]['url']

            result.append(songData)
            songData = {}

        return result

    # Return a list of audio features + track and artist name for user's top tracks
    def parseAudioFeatures(self, limit=20):
        data = {}
        result = []
        topTracks = self.spotifyObject.current_user_top_tracks(limit=limit)
        for item in topTracks['items']:
            uri = item['uri']
            audioFeatures = self.getAudioFeatures(uri)

            data['name'] = item['name']
            data['artist'] = item['artists'][0]['name']
            data['uri'] = audioFeatures[0]['uri']
            data['danceability'] = audioFeatures[0]['danceability']
            data['energy'] = audioFeatures[0]['energy']
            data['key'] = audioFeatures[0]['key']
            data['loudness'] = audioFeatures[0]['loudness']
            data['mode'] = audioFeatures[0]['mode']
            data['speechiness'] = audioFeatures[0]['speechiness']
            data['acousticness'] = audioFeatures[0]['acousticness']
            data['instrumentalness'] = audioFeatures[0]['instrumentalness']
            data['liveness'] = audioFeatures[0]['liveness']
            data['valence'] = audioFeatures[0]['valence']
            data['tempo'] = audioFeatures[0]['tempo']

            result.append(data)
            data = {}

        return result

     
# Use this if you want to print json files nicely
# print(json.dumps(VARIABLE, sort_keys=True, indent=4))

# Initialize the SpotifyManager class with the specified Spotify User ID
spManager = SpotifyManager('12160864262')

# example for using parseAudioFeatures():
# print(json.dumps(spManager.parseAudioFeatures(1), sort_keys=False, indent=4))

# example for using getRecommendations() - uri: spotify:track:1uRxyAup7OYrlh2SHJb80N
# print(json.dumps(spManager.getRecommendations(['spotify:track:1uRxyAup7OYrlh2SHJb80N']), sort_keys=True, indent=4))
