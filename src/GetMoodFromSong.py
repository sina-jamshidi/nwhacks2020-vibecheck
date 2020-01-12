import requests
import json

class GetMoodFromSong():
    def __init__(self):
        self.scoring_uri = 'http://aeb2b9c9-dbd7-4a23-98ec-b8b34d2a44a4.westus2.azurecontainer.io/score'


    def _format_data(self, songs):
        output = []
        for song in songs:
            data = [song['tempo'], song['energy'], song['danceability'], song['liveness'], \
                 song['valence'], 200, song['acousticness'], song['speechiness']]
            output.append(data)

        return {'data': output}



    def _getMood(self, songs):
        request = self._format_data(songs)

        # Convert to JSON string
        input_data = json.dumps(request)

        # Set the content type
        headers = {'Content-Type': 'application/json'}

        # Make the request and display the response
        resp = requests.post(self.scoring_uri, input_data, headers=headers)

        string = resp.json()
        json_obj = json.loads(string)

        return json_obj['result']

    def getMatches(self, songs, journal_mood):
        moods = self._getMood(songs)

        indices = []
        for i, mood in enumerate(moods):
            if mood == journal_mood:
                indices.append(i)
        
        return indices

