import sys
import time
sys.path.append('.')

from tools.lips import Lips

lip = Lips()
def random_text():
    for i in range(6):

        yield f'Hello world {i}.'
        time.sleep(1)
        
lip.speak(random_text())