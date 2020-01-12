from SpeechToText import STT
import paralleldots
import numpy as np

class GetEmotion():
    def __init__(self):
        self.api_key = "oCE90SarO5dry0aFG8UbsikB7FPkJRLSqaOgwSgJMHY"
        paralleldots.set_api_key(self.api_key)

    def getEmotionFromText(self, text):
        predictions = paralleldots.emotion(text)
        max_pred = 0
        emotion = ""
        for key in predictions['emotion'].keys():
            if predictions['emotion'][key] > max_pred:
                max_pred = predictions['emotion'][key]
                emotion = key.lower()
        return emotion

    def getBatchEmotionFromText(self, texts):
        predictions = paralleldots.batch_emotion(texts)
        emotions = []
        for prediction in predictions['emotion']:
            max_pred = 0
            emotion = ""
            for key in prediction.keys():
                if prediction[key] > max_pred:
                    max_pred = prediction[key]
                    emotion = key.lower()
            emotions.append(emotion)
        return emotions

    def getEmotionFromSpeech(self):
        my_stt = STT()
        result = my_stt.speech_to_text()

        print(' '.join(result))

        emotion = self.getEmotionFromText(result)

        print("detected emotion is: ", emotion)
        return (emotion, ' '.join(result))



# sample output from paralleldots.emotion(text)
# {'emotion': {'Excited': 0.0042200184, 'Angry': 0.1028312056, 'Sad': 0.692858962, 'Happy': 0.0029329932, 'Bored': 0.0119922102, 'Fear': 0.1851646106}}
