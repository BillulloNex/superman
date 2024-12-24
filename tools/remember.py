import chromadb



class Memory:
    def __init__(self, name='memory'):
        client = chromadb.HttpClient()
        self.collection = client.get_or_create_collection(name)
    
    def add(self, prompt, answer):
        self.collection.add(
            documents=[
                f"Question: {prompt}, Answer: {answer}",
            ],
            metadatas=[{'type': 'qna'}],
            ids = [f"{prompt}"]
            )
        return True
    def retrieve(self, query, n=5):
        result = self.collection.query(
            query_texts=[query],
            n_results=n,
        )
        return result
    def forget(self, key):
        pass
    
    def clear(self):
        pass


mem = Memory()
mem.add('What is the capital of France?', 'Paris')
mem.add('What is the capital of Vietnam?', 'Hanoi')
mem.add('Who is the best dog?', 'France')
print(mem.retrieve('What is the capital of France?', n=2))