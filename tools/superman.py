from ollama import chat
from ollama import ChatResponse

class Superman:
    def __init__(self, model = 'qwen2.5:0.5b', name="Clark Kent", personality="Always encouraging others towards greatness"):
        self.introduction = f'''
You are an honest person known as {name}, and your personality is {personality}. Keep your answer to under 100 words.
'''
        self.model = model
        self.messages = []
        self.messages.append(
            {'role': 'system', 'content': self.introduction}
        )
        

    def answer(self, prompt, web_context = '', file_context = '', memory_context = '', feeling_context = ''):
        if web_context != '':
            web_context = f'/nSupporting information from the web: {web_context}/n'
        if file_context != '':
            file_context = f'/nSupporting information from your files: {file_context}/n'
        if memory_context != '':
            memory_context = f'/nSupporting information from your memory: {memory_context}/n'
        return self.talk(prompt = prompt, context = f'{web_context} {file_context} {memory_context} {feeling_context}')
        
    
    def collect_full_message(self, stream):
        full_message = ''
        for chunk in stream:
            content = chunk['message']['content']
            yield content
            full_message += content
            if chunk is None or content is None:
                print('donezo')
                return False
                break
        self.messages.append({'role': 'assistant', 'content': full_message})
        return full_message

    def talk(self, prompt, context=''):
        self.messages.append({'role': 'user', 'content': f'{context} {prompt}'})
        stream = chat(
            model=self.model,
            messages=self.messages,
            stream=True,
        )

        return self.collect_full_message(stream)
        
'''
# atlas = Superman(name='Princess Bubblegum', model = 'smollm2:360m', personality='A crazy and sexy female scientist in a candy kingdom')

# while True:
#     print('\n')
#     prompt = input("Enter your prompt: ")
#     if prompt == 'exit':
#         break
#     atlas.answer(prompt)

#for chunk in atlas.answer('What is the meaning of life?'):
#     print(chunk)
'''