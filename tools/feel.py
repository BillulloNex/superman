from llmware.agents import LLMfx

class Feeling:
    def __init__(self):
        self.agent = LLMfx()
    def analyze(self, message):
        self.agent.load_work(message)
        self.agent.load_tool_list([
            'sentiment',
            'topics',
            'emotions'
        ])
        sentiment = self.agent.sentiment()['llm_response']
        topics = self.agent.topics()['llm_response']
        emotions = self.agent.emotions()['llm_response']
        return {
            'sentiment': sentiment,
            'topics': topics,
            'emotions': emotions
        }
    

feel = Feeling()
vibe = feel.analyze('my dog just laughed from a happy marriage')
print(vibe)