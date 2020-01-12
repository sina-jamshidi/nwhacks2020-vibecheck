from SpotifyManager import SpotifyManager

sm = SpotifyManager("12160864262")

# result = sm.spotifyObject.search("say something a great big world", limit=2, type='track')


song = sm.spotifyObject.track("5TvE3pk05pyFIGdSY9j4DJ")


data = {}
result = []
for item in [song]:
    uri = item['uri']
    audioFeatures = sm.getAudioFeatures(uri)

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

print(result)
