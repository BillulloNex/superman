from langchain_community.tools import BraveSearch
from dotenv import load_dotenv
import os
import requests
import json
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex

load_dotenv()

class Web:
    def __init__(self):
        #self.brave_tool = BraveSearch.from_api_key(api_key=os.environ["BRAVE_SEARCH_API"], search_kwargs={"count": 3})
        self.headers = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip',
        'X-Subscription-Token': os.environ["BRAVE_SEARCH_API"],
        
    }

    def brave_search(self, query):
        #result = self.brave_tool.run(query)
        url = f"https://api.search.brave.com/res/v1/web/search?q={query}&summary=1&count=3"
        search = requests.get(url, headers=self.headers)
        search = search.json()
        result = {}
        result['query'] = query
        result['snippets'] = []
        for web_result in search['web']['results']:
            if 'extra_snippets' in web_result:
                for snippet in web_result['extra_snippets']:
                    result['snippets'].append(snippet)
        with open('search_result.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        
        return result
    def facts(self, query):
        result = self.brave_search(query)
        context = 'Here are some facts and contextual information: '
        for snippet in result['snippets']:
            context = context + snippet + '\n'
        
        return context
    def cache(self, query, result):
        pass

class InternalDoc:
    def __init__(self):
        # Load documents from a directory
        self.documents = SimpleDirectoryReader("./data").load_data()
        # Create an index from the documents
        index = VectorStoreIndex.from_documents(self.documents)
        # Create a query engine
        self.query_engine = index.as_query_engine()

    def search(self, query):
        # Query the system
        response = self.query_engine.query(query)
        print(response)

# web = Web()
# print(web.facts("What is the capital of France?"))
doc = InternalDoc()
doc.search('What did Environmental Sustainability Report include?')












