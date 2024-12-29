from hardware.buttons import Button
from tools.ear import Ear
from tools.lips import Lips
from tools.superman import Superman
import os
import warnings
warnings.filterwarnings('ignore')

talk_button = Button(26)
# listen = Ear()

ear = Ear()
lip = Lips()
atlas = Superman(name='Princess Bubblegum', model = 'qwen2.5:0.5b', personality='Crazy and sexy')

transcription_pending = False

for chunk in talk_button.monitor():
    # print(chunk)
    if chunk == True:
        ear.start_recording()
        transcription_pending = True
    elif chunk == False and transcription_pending:
        ear.stop_recording()
        # After stopping recording, transcribe the audio only once
        audio_path = "test.wav"
        if audio_path and os.path.exists(audio_path):
            text = ear.transcribe_recording()
            print('speaking')
            lip.speak(atlas.answer(text))
        transcription_pending = False
    # print(ear.get_status())
