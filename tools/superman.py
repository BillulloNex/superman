from ollama import chat
from ollama import ChatResponse

class Superman:
    def __init__(self, model = 'qwen2.5:0.5b', name="Clark Kent", personality="Always encouraging others towards greatness"):
        self.introduction = f'''
You are an honest person known as {name}, and your personality is {personality}.
'''
        self.model = model
        

    def answer(self, prompt, web_context = '', file_context = '', memory_context = '', feeling_context = ''):
        if web_context != '':
            web_context = f'/nSupporting information from the web: {web_context}/n'
        if file_context != '':
            file_context = f'/nSupporting information from your files: {file_context}/n'
        if memory_context != '':
            memory_context = f'/nSupporting information from your memory: {memory_context}/n'
        return self.talk(prompt = prompt, context = f'{web_context} {file_context} {memory_context} {feeling_context}')
        

    def talk(self, prompt, context=''):
        stream = chat(
            model=self.model,
            messages=[{'role': 'user', 'content': f'{self.introduction} {context} {prompt}'}],
            stream=True,
            )
        return stream
        for chunk in stream:
            print(chunk['message']['content'], end='', flush=True)
        
atlas = Superman(name='Princess Bubblegum', personality='A crazy and sexy female scientist in a candy kingdom')

for chunk in atlas.answer('Do you think engineers are cool?'):
    print(chunk['message']['content'], end='', flush=True)