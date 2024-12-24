import whisper
import time
class Ear:
    def __init__(self):
        self.model = whisper.load_model('tiny.en')
    def transcribe(self, audio_file):
        begin = time.time()
        result = self.model.transcribe(audio_file)
        print(result['text'])
        print(f'Time taken: {time.time() - begin} seconds')

ear = Ear()
ear.transcribe('recording.m4a')