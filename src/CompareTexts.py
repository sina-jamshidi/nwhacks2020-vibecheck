import paralleldots
import numpy as np
import os
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials
from GetEmotionFromText import GetEmotion
class CompareTexts():
    def __init__(self, journal_emotion):
        self.emotion_journal = journal_emotion
        self.getEmotion = GetEmotion()
        self.subscription_key = "ec69a4d6cb1f42e99bea0ba99f02b3b4"
        self.endpoint = "https://nwhacks-textanalytics.cognitiveservices.azure.com/"

    def authenticateClient(self):
        credentials = CognitiveServicesCredentials(self.subscription_key)
        text_analytics_client = TextAnalyticsClient(
            endpoint=self.endpoint, credentials=credentials)
        return text_analytics_client

    def compareTexts(self, journal, songs):
        Analytics_client = self.authenticateClient()

        for song in songs:
            if song['lyrics'] is None:
                song['lyrics'] == "does not apply"

        try:
            documents = [
                {"id": "1", "language": "en", "text": journal},
                {"id": "2", "language": "en",
                    "text": songs[0]['lyrics']},
                {"id": "3", "language": "en",
                    "text": songs[1]['lyrics']},
                {"id": "4", "language": "en",
                    "text": songs[2]['lyrics']},
                {"id": "5", "language": "en",
                    "text": songs[3]['lyrics']},
                {"id": "6", "language": "en",
                    "text": songs[4]['lyrics']},
                {"id": "7", "language": "en",
                    "text": songs[5]['lyrics']},
                {"id": "8", "language": "en",
                    "text": songs[6]['lyrics']},
                {"id": "9", "language": "en",
                    "text": songs[7]['lyrics']},
                {"id": "10", "language": "en",
                    "text": songs[8]['lyrics']},
                {"id": "11", "language": "en",
                    "text": songs[9]['lyrics']},
            ]

            response = Analytics_client.sentiment(documents=documents)
            sentiments = []
            for document in response.documents:
                sentiments.append(document.score)

        except Exception as err:
            print("Encountered exception. {}".format(err))

        semanticAnalysis_journal = sentiments[0]
        semanticAnalysis_lyrics = sentiments[1:]

        semantic_differences = abs(semanticAnalysis_journal - np.array(semanticAnalysis_lyrics))

        # map emotions
        lyrics_list = [song['lyrics'] for song in songs]
        emotion_lyrics = self.getEmotion.getBatchEmotionFromText(lyrics_list)

        emotions = [self.emotion_journal] + emotion_lyrics
        emotion_int = []
        for emotion in emotions:
            if emotion == "sad":
                emotion_int.append(1)
            elif emotion == "angry":
                emotion_int.append(2)
            elif emotion == "fear" or emotion == "bored":
                emotion_int.append(3)
            elif emotion == "excited":
                emotion_int.append(4)
            else:
                emotion_int.append(5)
        emotion_journal_normalized = (emotion_int[0]-0)/5
        emotion_lyrics_normalized = (np.array(emotion_int[1:])-0)/5
        emotion_differences = abs(emotion_journal_normalized - emotion_lyrics_normalized)

        average_differences = (semantic_differences + emotion_differences)/2

        top_song_index = np.argmax(average_differences)

        top_song = songs[top_song_index]

        return top_song


