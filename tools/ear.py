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
    



# ear = Ear()
# ear.transcribe('recording.m4a')

import pyaudio
import numpy as np
import wave

import pyaudio
import numpy as np
import wave
import keyboard
import threading

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
WAVE_OUTPUT_FILENAME = 'output.wav'
volume_factor = 2.0  # Increase volume by doubling (adjust as needed)

p = pyaudio.PyAudio()

frames = []
recording = False
stop_recording = False

def record_audio():
    global frames, recording, stop_recording
    
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    while not stop_recording:
        if recording:
            data = stream.read(CHUNK)
            audio_data = np.frombuffer(data, dtype=np.int16)
            audio_data = (audio_data * volume_factor).clip(-32768, 32767).astype(np.int16)
            modified_data = audio_data.tobytes()
            frames.append(modified_data)

    stream.stop_stream()
    stream.close()

print("Press 's' to start recording and 'q' to stop and save.")

# Start the recording thread
record_thread = threading.Thread(target=record_audio)
record_thread.start()

# Wait for 's' key to start recording
keyboard.wait('s')
print("Recording started. Press 'q' to stop.")
recording = True

# Wait for 'q' key to stop recording
keyboard.wait('q')
print("Recording stopped. Saving file...")
recording = False
stop_recording = True

# Wait for the recording thread to finish
record_thread.join()

p.terminate()

# Save the recorded data as a WAV file
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

print(f"Audio saved as {WAVE_OUTPUT_FILENAME}")
