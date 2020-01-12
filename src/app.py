from flask import Flask, request, jsonify
from GetEmotionFromText import GetEmotion
from GeniusManager import GeniusManager
from SpotifyManager import SpotifyManager
from GetMoodFromSong import GetMoodFromSong
from CompareTexts import CompareTexts

import os
from flask_cors import CORS
from flask import jsonify

app = Flask(__name__)
CORS(app)

@app.route("/record/", methods=['GET'])
def record_voice():
    getEmotion = GetEmotion()
    journal_emotion, journal_entry = getEmotion.getEmotionFromSpeech()

    return jsonify({"journal_emotion":str(journal_emotion), "journal_entry":str(journal_entry)})



@app.route("/get_song/", methods=['GET'])
def get_playlist():
    journal_emotion = request.args.get('journalem')
    journal_entry = request.args.get('journalen')

    print(journal_emotion)
    print(journal_entry)

    getEmotion = GetEmotion()
    spotify = SpotifyManager("12160864262")
    moodFromSong = GetMoodFromSong()
    genius = GeniusManager()

    top_songs = spotify.getTopTracks(limit=10)
    top_song_features = spotify.getAudioFeatures(top_songs)

    matching_moods_indices = moodFromSong.getMatches(top_song_features, journal_emotion)

    matching_songs = []
    for i, song in enumerate(top_songs):
        if i in matching_moods_indices:
            matching_songs.append(song['uri'])

    if len(matching_songs) == 0:
        song = getMatchingSongs(journal_emotion)
        matching_songs.append(song['uri'])

    recommended_songs = spotify.getRecommendations(matching_songs, limit=10)

    lyrics = genius.getLyrics(recommended_songs)

    compareTexts = CompareTexts(journal_emotion)

    top_song = compareTexts.compareTexts(journal_entry, lyrics)

    return jsonify(top_song)

def getMatchingSongs(emotion):
    if emotion == "happy":
        song = {'name': 'Happy - From "Despicable Me 2"', 'artist': 'Pharrell Williams', 'uri': 'spotify:track:60nZcImufyMA1MKQY3dcCH', 'danceability': 0.647, 'energy': 0.822, 'key': 5, 'loudness': -4.662, 'mode': 0, 'speechiness': 0.183, 'acousticness': 0.219, 'instrumentalness': 0, 'liveness': 0.0908, 'valence': 0.962, 'tempo': 160.019}
    elif emotion == "angry":
        song = {'name': 'The Way I Am', 'artist': 'Eminem', 'uri': 'spotify:track:2sGSId790ABFzGXx9VEdwl', 'danceability': 0.671, 'energy': 0.852, 'key': 7, 'loudness': -3.315, 'mode': 1, 'speechiness': 0.272, 'acousticness': 0.137, 'instrumentalness': 0, 'liveness': 0.311, 'valence': 0.325, 'tempo': 87.027}
    elif emotion == "bored" or emotion == "fear":
        song = {'name': 'Hide and Seek', 'artist': 'Imogen Heap', 'uri': 'spotify:track:121so7t3AeX6nLMvxy9ZP9', 'danceability': 0.452, 'energy': 0.179, 'key': 9, 'loudness': -11.165, 'mode': 1, 'speechiness': 0.0824, 'acousticness': 0.899, 'instrumentalness': 0, 'liveness': 0.178, 'valence': 0.103, 'tempo': 121.488}
    elif emotion == "excited":
        song = {'name': 'Sandstorm - Radio Edit', 'artist': 'Darude', 'uri': 'spotify:track:24CXuh2WNpgeSYUOvz14jk', 'danceability': 0.539, 'energy': 0.98, 'key': 11, 'loudness': -8.18, 'mode': 0, 'speechiness': 0.0469, 'acousticness': 0.169, 'instrumentalness': 0.982, 'liveness': 0.084, 'valence': 0.522, 'tempo': 136.087}
    else:
        song = {'name': 'Say Something', 'artist': 'A Great Big World', 'uri': 'spotify:track:5TvE3pk05pyFIGdSY9j4DJ', 'danceability': 0.407, 'energy': 0.147, 'key': 2, 'loudness': -8.822, 'mode': 1, 'speechiness': 0.0355, 'acousticness': 0.857, 'instrumentalness': 2.89e-06, 'liveness': 0.0913, 'valence': 0.0765, 'tempo': 141.284}
    return song

if __name__ == "__main__":
    app.run()