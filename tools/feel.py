from llmware.agents import LLMfx

class Feeling:
    def __init__(self):
        self.agent = LLMfx()
    def analyze(self, message):
        self.agent.load_work(message)
        self.agent.load_tool_list([
            'sentiment',
            'topics',
            'emotions',
            'intent'
        ])
        sentiment = self.agent.sentiment()['llm_response']
        topics = self.agent.topics()['llm_response']
        emotions = self.agent.emotions()['llm_response']
        intent = self.agent.intent()['llm_response']
        return {
            'sentiment': sentiment,
            'topics': topics,
            'emotions': emotions,
            'intent': intent
        }
    

feel = Feeling()
vibe = feel.analyze('I want to stab my ex-boyfriend and marry him happily ever after')
print(vibe)