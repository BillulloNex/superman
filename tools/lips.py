import requests
import subprocess
import json
import re
import threading
import queue
import sys

class PiperTTS:
    def __init__(self):
        self.model = "en_US-lessac-medium.onnx"
        self.audio_queue = queue.Queue(maxsize=3)  # Buffer for pre-generated audio
        self.current_process = None
        
    def generate_audio(self, text):
        """Generate audio data without playing it"""
        if not text.strip():
            return None
            
        try:
            # Run piper to generate raw audio
            piper_process = subprocess.Popen(
                ["piper", "--model", self.model, "--output_raw"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Write text and get audio data
            piper_process.stdin.write(text.strip().encode())
            piper_process.stdin.flush()
            piper_process.stdin.close()
            
            audio_data = piper_process.stdout.read()
            piper_process.wait()
            
            return audio_data
            
        except Exception as e:
            print(f"Audio Generation Error: {str(e)}")
            return None
    
    def play_audio(self, audio_data):
        """Play pre-generated audio data"""
        if audio_data:
            try:
                # Play the audio data using aplay
                aplay_process = subprocess.Popen(
                    ["aplay", "-r", "22050", "-f", "S16_LE", "-c", "1"],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                
                aplay_process.stdin.write(audio_data)
                aplay_process.stdin.close()
                aplay_process.wait()
                
            except Exception as e:
                print(f"Audio Playback Error: {str(e)}")

class SentenceBuffer:
    def __init__(self):
        self.buffer = ""
        self.sentence_pattern = re.compile(r'(?<=[.!?])\s+(?=[A-Z])|(?<=[.!?])$')
        self.abbreviations = {'Mr.', 'Mrs.', 'Dr.', 'Ms.', 'Prof.', 'Sr.', 'Jr.', 'vs.', 'e.g.', 'i.e.'}
    
    def is_abbreviation(self, text):
        for abbr in self.abbreviations:
            if text.endswith(abbr):
                return True
        return False
    
    def add_text(self, text):
        self.buffer += text
        
        sentences = []
        last_end = 0
        
        for match in self.sentence_pattern.finditer(self.buffer):
            end_pos = match.end()
            sentence = self.buffer[last_end:end_pos].strip()
            
            if sentence and not self.is_abbreviation(sentence):
                sentences.append(sentence)
                last_end = end_pos
        
        if sentences:
            self.buffer = self.buffer[last_end:]
        
        return sentences
    
    def flush(self):
        if self.buffer.strip():
            final_text = self.buffer
            self.buffer = ""
            return final_text
        return None

class TextProcessor:
    def __init__(self, audio_queue, print_queue):
        self.audio_queue = audio_queue
        self.print_queue = print_queue
        self.sentence_buffer = SentenceBuffer()
        self.tts = PiperTTS()
        
    def process_text(self, text):
        self.print_queue.put(text)
        
        sentences = self.sentence_buffer.add_text(text)
        for sentence in sentences:
            # Generate audio data and add to queue
            audio_data = self.tts.generate_audio(sentence)
            if audio_data:
                self.audio_queue.put((sentence, audio_data))
    
    def finish(self):
        final_text = self.sentence_buffer.flush()
        if final_text:
            audio_data = self.tts.generate_audio(final_text)
            if audio_data:
                self.audio_queue.put((final_text, audio_data))
        self.audio_queue.put(None)  # Signal completion

def text_display_worker(print_queue):
    print('text in')
    while True:
        text = print_queue.get()
        if text is None:
            break
        print(text, end='', flush=True)
        print_queue.task_done()
    print('text out')
    return True

def audio_player_worker(audio_queue):
    print('audio worker in')
    """Worker thread that plays pre-generated audio"""
    tts = PiperTTS()
    while True:
        item = audio_queue.get()
        if item is None:
            break
        
        sentence, audio_data = item
        tts.play_audio(audio_data)
        audio_queue.task_done()
    print('audio worker out')
    return True

class Lips:
    def __init__(self):
        # Initialize queues
        self.audio_queue = queue.Queue(maxsize=3)  # Limit buffer size
        self.print_queue = queue.Queue()
        
        # Initialize text processor
        self.text_processor = TextProcessor(self.audio_queue, self.print_queue)
        
        # Ensure audio device is ready
        try:
            subprocess.run(["amixer", "sset", "PCM", "unmute"], check=False)
            subprocess.run(["amixer", "sset", "PCM", "100%"], check=False)
        except:
            print("Error: Unable to set audio volume.")
        
        # Start worker threads
        audio_thread = threading.Thread(target=audio_player_worker, args=(self.audio_queue,))
        display_thread = threading.Thread(target=text_display_worker, args=(self.print_queue,))
        audio_thread.daemon = True
        display_thread.daemon = True
        
        audio_thread.start()
        display_thread.start()
    def speak(self, stream):
        
        try:
            for text_chunk in stream:
                if text_chunk == '' :
                    break
            
                self.text_processor.process_text(text_chunk)
            # self.text_processor.finish()
            
            self.audio_queue.put(None)
            self.print_queue.put(None)
            # print('print queue joined')
            # print(f"Audio queue size: {self.audio_queue.qsize()}")
            # print("Queue contents before join:")
            # queue_copy = list(self.audio_queue.queue)
            # print(queue_copy)
            self.audio_queue.task_done()
            print('done')
            # self.audio_queue.join()
            print(f"Audio queue size after join: {self.audio_queue.qsize()}")
            print('audio queue joined')
            self.print_queue.task_done()
            # self.print_queue.join()
            print('tadone')

            
        except KeyboardInterrupt:
            print("\nStopping program...")
        except Exception as e:
            print(f"\nAn error occurred: {e}")
        finally:
            print("Exiting program...")
            
            # Ensure threads are properly terminated  
            self.text_processor.finish()
            
            return True
            
        print('exit for good')
        return True
    def hi(self, text):
        self.text_processor.process_text(text)
        self.text_processor.finish()
        self.audio_queue.put(None)
        self.print_queue.put(None)
        print('print queue joined')
        print(f"Audio queue size: {self.audio_queue.qsize()}")
        print("Queue contents before join:")
        queue_copy = list(self.audio_queue.queue)
        print(queue_copy)
        self.audio_queue.task_done()
        print('done')
        # self.audio_queue.join()
        print(f"Audio queue size after join: {self.audio_queue.qsize()}")
        print('audio queue joined')
        self.print_queue.task_done()
        # self.print_queue.join()
        print('tadone')


'''def random_text():
    for i in range(2):
        yield f'Hello world {i}.'
lip = Lips()
# lip.hi('hi i am bubble gum')
# lip.hi('and you look rather sexy')
lip.speak(random_text())
lip2 = Lips()
lip2.speak(random_text())
  
'''
'''
from superman import Superman

atlas = Superman(name='Princess Bubblegum', model = 'qwen2.5:0.5b', personality='Crazy and sexy')

lip.speak(atlas.answer('What is the meaning of life?'))



lip.speak(random_text())
'''